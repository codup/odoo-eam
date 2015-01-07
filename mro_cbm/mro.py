# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 CodUP (<http://codup.com>).
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
        ('pm', 'Preventive'),
        ('cbm', 'Predictive')
    ]
    
    _columns = {
        'maintenance_type': fields.selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True, readonly=True, states={'draft': [('readonly', False)]}),
    }

    def replan_cbm(self, cr, uid, context=None):
        rule_obj = self.pool.get('mro.cbm.rule')
        asset_obj = self.pool.get('asset.asset')
        ids = rule_obj.search(cr, uid, [])
        for rule in rule_obj.browse(cr,uid,ids,context=context):
            asset_ids = asset_obj.search(cr, uid, [('category_id', '=', rule.category_id.id)])
            for asset in asset_obj.browse(cr,uid,asset_ids,context=context):
                for gauge in asset.gauge_ids:
                    if gauge.name != rule.parameter_id or gauge.state != 'reading': continue
                    self.planning_strategy_2(cr, uid, asset, gauge, rule, context=context)
        return True

    def planning_strategy_2(self, cr, uid, asset, gauge, rule, context=None):
        gauge_line_obj = self.pool.get('mro.gauge.line')
        last_read = gauge_line_obj.search(cr, uid, [('gauge_id', '=', gauge.id)], limit=1, order='date desc')
        gauge_reads = gauge_line_obj.browse(cr, uid, last_read)
        if (rule.is_limit_min and rule.limit_min>gauge_reads.value) or (rule.is_limit_max and rule.limit_max<gauge_reads.value):
            task = rule.task_id
            order_ids = self.search(cr, uid, 
                [('asset_id', '=', asset.id),
                ('state', 'not in', ('draft','cancel')),
                ('maintenance_type', '=', 'cbm'),
                ('task_id', '=', task.id)],
                limit=1, order='date_execution desc')
            if len(order_ids) > 0:
                date = self.browse(cr, uid, order_ids[0], context=context).date_execution
                Do = 1.0*calendar.timegm(time.strptime(date, "%Y-%m-%d %H:%M:%S"))
                Dg = 1.0*calendar.timegm(time.strptime(gauge_reads.date, "%Y-%m-%d"))
                if Do>Dg: return True
            order_ids = self.search(cr, uid, 
                [('asset_id', '=', asset.id),
                ('state', '=', 'draft'),
                ('maintenance_type', '=', 'cbm'),
                ('task_id', '=', task.id)],
                order='date_execution')
            Tp = fields.datetime.now()
            values = {
                'date_planned':Tp,
                'date_scheduled':Tp,
                'date_execution':Tp,
                'origin': rule.name,
                'state': 'draft',
                'maintenance_type': 'cbm',
                'asset_id': asset.id,
            }
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
            if len(order_ids) > 0:
                order = self.browse(cr, uid, order_ids[0], context=context)
                values['parts_lines'] = parts_lines + [[2,line.id] for line in order.parts_lines]
                self.write(cr, uid, [order.id], values)
                return True
            values['parts_lines'] = parts_lines
            self.create(cr, uid, values)
        return True


class mro_task(osv.osv):
    _inherit = 'mro.task'

    MAINTENANCE_TYPE_SELECTION = [
        ('cm', 'Corrective'),
        ('pm', 'Preventive'),
        ('cbm', 'Predictive')
    ]

    _columns = {
        'maintenance_type': fields.selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: