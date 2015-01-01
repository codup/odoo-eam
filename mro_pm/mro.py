# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-2015 CodUP (<http://codup.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
import calendar

from openerp.osv import fields, osv

class mro_order(osv.osv):
    _inherit = 'mro.order'
    
    MAINTENANCE_TYPE_SELECTION = [
        ('bm', 'Breakdown'),
        ('cm', 'Corrective'),
        ('pm', 'Preventive')
    ]
    
    _columns = {
        'maintenance_type': fields.selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True, readonly=True, states={'draft': [('readonly', False)]}),
    }
    
    def find_step(self, start, end, tmin, tmax):
        M = round(2*(end - start)/(tmin + tmax),0)
        if M != 0:
            step = (end - start)/M
            if step < tmin:
                M = M - 1
                if M != 0:
                    step = (end - start)/M
                if step < tmin or step > tmax: step = tmin
            elif step > tmax:
                M = M + 1
                step = (end - start)/M
                if step < tmin or step > tmax: step = tmax
        else: step = tmin
        return step

    def replan_pm(self, cr, uid, context=None):
        rule_obj = self.pool.get('mro.pm.rule')
        ids = rule_obj.search(cr, uid, [])
        for rule in rule_obj.browse(cr,uid,ids,context=context):
            tasks = [x for x in rule.pm_rules_line_ids]
            asset = rule.asset_id
            meter = rule.meter_id
            horizon = rule.horizon
            origin = rule.name
            self.planning_strategy_1(cr, uid, asset, meter, tasks, horizon, origin, context=context)
        return True

    def planning_strategy_1(self, cr, uid, asset, meter, tasks, horizon, origin, context=None):
        meter_obj = self.pool.get('mro.pm.meter')
        if meter.state != 'reading' or not len(tasks): return True
        tasks.sort(lambda y,x: cmp(x.meter_interval_id.interval_max, y.meter_interval_id.interval_max))
        K = 3600.0*24
        hf = len(tasks)-1
        lf = 0
        task_ids = []
        Ci = []
        Imin = []
        Imax = []
        Si = []
        Dmin = []
        Dmax = []
        Dopt = []
        for task in tasks:
            task_ids.append(task.task_id.id)
            order_ids = self.search(cr, uid, 
                [('asset_id', '=', asset.id),
                ('state', 'not in', ('draft','cancel')),
                ('maintenance_type', '=', 'pm'),
                ('task_id', 'in', task_ids)],
                limit=1, order='date_execution desc')
            if len(order_ids) > 0:
                date = self.browse(cr, uid, order_ids[0], context=context).date_execution
                Ci.append(K*meter_obj.get_reading(cr, uid, meter.id, date))
            else: Ci.append(0)
            Imin.append(K*task.meter_interval_id.interval_min)
            Imax.append(K*task.meter_interval_id.interval_max)
            Si.append(0)
            Dmin.append(0)
            Dmax.append(0)
            Dopt.append(0)
        C = K*meter.total_value
        Dc = 1.0*calendar.timegm(time.strptime(meter.date, "%Y-%m-%d"))
        N = meter.utilization
        Hp = 3600.0*24*31*horizon
        Dn = 1.0*calendar.timegm(time.strptime(time.strftime('%Y-%m-%d',time.gmtime()),"%Y-%m-%d"))
        Si[lf] = Imin[lf]
        for i in range(hf):
            Si[i+1] = self.find_step(Ci[i+1], Ci[i] + Si[i], Imin[i+1], Imax[i+1])
        for i in range(hf+1):
            Dmin[i] = Dc + (Imin[i] - C + Ci[i])/N
            Dmax[i] = Dmin[i] + (Imax[i] - Imin[i])/N
            Dopt[i] = Dc + (Si[i] - C + Ci[i])/N
        Dp = Dopt[hf]
        for i in range(hf):
            if Dp > Dmax[i]: Dp = Dmax[i]
        if Dp<Dn: Dp=Dn
        Cp = C + (Dp - Dc)*N
        delta = Cp - Ci[hf]
        order_ids = self.search(cr, uid, 
            [('asset_id', '=', asset.id),
            ('state', '=', 'draft'),
            ('maintenance_type', '=', 'pm'),
            ('task_id', 'in', task_ids)],
            order='date_execution')
        for order in self.browse(cr, uid, order_ids, context=context):
            Tp = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(Dp))
            values = {
                'date_planned':Tp,
                'date_scheduled':Tp,
                'date_execution':Tp,
                'origin': origin,
                'state': 'draft',
                'maintenance_type': 'pm',
                'asset_id': asset.id,
            }
            task = tasks[hf].task_id
            Ci[hf] = Cp
            Si[hf] = self.find_step(Ci[hf], Ci[hf-1] + Si[hf-1], Imin[hf], Imax[hf])
            for i in range(hf):
                if Dmin[i] < Dp + (Si[hf]-Imax[i]+Imin[i])/N:
                    task = tasks[i].task_id
                    for j in range(hf-i):
                        Ci[i+j] = Cp
                    for j in range(hf-i):
                        Si[i+j] = self.find_step(Ci[i+j], Ci[i+j-1] + Si[i+j-1], Imin[i+j], Imax[i+j])
                        Dmin[i+j] = Dp + Imin[i+j]/N
                        Dmax[i+j] = Dp + Imax[i+j]/N
                        Dopt[i+j] = Dp + Si[i+j]/N
                    break
            Si[hf] = self.find_step(Ci[hf], Ci[hf-1] + Si[hf-1], Imin[hf], Imax[hf])
            Dmin[hf] = Dp + Imin[hf]/N
            Dmax[hf] = Dp + Imax[hf]/N
            Dopt[hf] = Dp + Si[hf]/N
            values['task_id'] = task.id
            values['description'] = task.name
            values['tools_description'] = task.tools_description
            values['labor_description'] = task.labor_description
            values['operations_description'] = task.operations_description
            values['documentation_description'] = task.documentation_description
            parts_lines = [[2,line.id] for line in order.parts_lines]
            for line in task.parts_lines:
                parts_lines.append([0,0,{
                    'name': line.name,
                    'parts_id': line.parts_id.id,
                    'parts_qty': line.parts_qty,
                    'parts_uom': line.parts_uom.id,
                    }])
            values['parts_lines'] = parts_lines
            self.write(cr, uid, [order.id], values)
            Dp = Dopt[hf]
            for i in range(hf):
                if Dp > Dmax[i]: Dp = Dmax[i]
            Co = Cp
            Cp = C + (Dp - Dc)*N
            delta = Cp - Co
        Dhp = Dn + Hp
        while Dp < Dhp:
            Tp = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(Dp))
            values = {
                'date_planned':Tp,
                'date_scheduled':Tp,
                'date_execution':Tp,
                'origin': origin,
                'state': 'draft',
                'maintenance_type': 'pm',
                'asset_id': asset.id,
            }
            task = tasks[hf].task_id
            Ci[hf] = Cp
            Si[hf] = self.find_step(Ci[hf], Ci[hf-1] + Si[hf-1], Imin[hf], Imax[hf])
            for i in range(hf):
                if Dmin[i] < Dp + (Si[hf]-Imax[i]+Imin[i])/N:
                    task = tasks[i].task_id
                    for j in range(hf-i):
                        Ci[i+j] = Cp
                    for j in range(hf-i):
                        Si[i+j] = self.find_step(Ci[i+j], Ci[i+j-1] + Si[i+j-1], Imin[i+j], Imax[i+j])
                        Dmin[i+j] = Dp + Imin[i+j]/N
                        Dmax[i+j] = Dp + Imax[i+j]/N
                        Dopt[i+j] = Dp + Si[i+j]/N
                    break
            Si[hf] = self.find_step(Ci[hf], Ci[hf-1] + Si[hf-1], Imin[hf], Imax[hf])
            Dmin[hf] = Dp + Imin[hf]/N
            Dmax[hf] = Dp + Imax[hf]/N
            Dopt[hf] = Dp + Si[hf]/N
            values['task_id'] = task.id
            values['description'] = task.name
            values['tools_description'] = task.tools_description
            values['labor_description'] = task.labor_description
            values['operations_description'] = task.operations_description
            values['documentation_description'] = task.documentation_description
            parts_lines = []
            for line in task.parts_lines:
                parts_lines.append([0,0,{
                    'name': line.name,
                    'parts_id': line.parts_id.id,
                    'parts_qty': line.parts_qty,
                    'parts_uom': line.parts_uom.id,
                    }])
            values['parts_lines'] = parts_lines
            self.create(cr, uid, values)
            Dp = Dopt[hf]
            for i in range(hf):
                if Dp > Dmax[i]: Dp = Dmax[i]
            Co = Cp
            Cp = C + (Dp - Dc)*N
            delta = Cp - Co
        return True


class mro_task(osv.osv):
    _inherit = 'mro.task'
    
    MAINTENANCE_TYPE_SELECTION = [
        ('cm', 'Corrective'),
        ('pm', 'Preventive')
    ]
    
    _columns = {
        'maintenance_type': fields.selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True),
    }

    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: