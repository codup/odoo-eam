# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2017 CodUP (<http://codup.com>).
#
##############################################################################

import time
import calendar
from odoo import api, fields, models


class mro_order(models.Model):
    _inherit = 'mro.order'

    MAINTENANCE_TYPE_SELECTION = [
        ('bm', 'Breakdown'),
        ('cm', 'Corrective'),
        ('pm', 'Preventive')
    ]

    maintenance_type = fields.Selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True, readonly=True, states={'draft': [('readonly', False)]})

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
                if M != 0:
                    step = (end - start)/M
                if step < tmin or step > tmax: step = tmax
        else: step = tmin
        return step

    def replan_pm(self):
        rule_obj = self.env['mro.pm.rule']
        asset_obj = self.env['asset.asset']
        ids = rule_obj.search([])
        for rule in ids:
            tasks = [x for x in rule.pm_rules_line_ids]
            if not len(tasks): continue
            horizon = rule.horizon
            origin = rule.name
            for asset in rule.category_id.asset_ids:
                for meter in asset.meter_ids:
                    if meter.name != rule.parameter_id or meter.state != 'reading': continue
                    self.planning_strategy_1(asset, meter, tasks, horizon, origin)
        return True

    def planning_strategy_1(self, asset, meter, tasks, horizon, origin):
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
            order_ids = self.search(
                [('asset_id', '=', asset.id),
                ('state', 'not in', ('draft','cancel')),
                ('maintenance_type', '=', 'pm'),
                ('task_id', 'in', task_ids)],
                limit=1, order='date_execution desc')
            if len(order_ids) > 0:
                date = order_ids[0].date_execution
                Ci.append(K*meter.get_reading(date))
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
        order_ids = self.search(
            [('asset_id', '=', asset.id),
            ('state', '=', 'draft'),
            ('maintenance_type', '=', 'pm'),
            ('task_id', 'in', task_ids)],
            order='date_execution')
        for order in order_ids:
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
            order.write(values)
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
            self.create(values)
            Dp = Dopt[hf]
            for i in range(hf):
                if Dp > Dmax[i]: Dp = Dmax[i]
            Co = Cp
            Cp = C + (Dp - Dc)*N
            delta = Cp - Co
        return True


class mro_task(models.Model):
    _inherit = 'mro.task'

    MAINTENANCE_TYPE_SELECTION = [
        ('cm', 'Corrective'),
        ('pm', 'Preventive')
    ]

    maintenance_type = fields.Selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: