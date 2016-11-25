# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2015-2016 CodUP (<http://codup.com>).
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
        ('pm', 'Preventive'),
        ('cbm', 'Predictive')
    ]

    maintenance_type = fields.Selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True, readonly=True, states={'draft': [('readonly', False)]})

    def replan_cbm(self):
        rule_obj = self.env['mro.cbm.rule']
        asset_obj = self.env['asset.asset']
        ids = rule_obj.search([])
        for rule in ids:
            for asset in rule.category_id.asset_ids:
                for gauge in asset.gauge_ids:
                    if gauge.name != rule.parameter_id or gauge.state != 'reading': continue
                    self.planning_strategy_2(asset, gauge, rule)
        return True

    def planning_strategy_2(self, asset, gauge, rule):
        gauge_line_obj = self.env['mro.gauge.line']
        gauge_reads = gauge_line_obj.search([('gauge_id', '=', gauge.id)], limit=1, order='date desc')[0]
        if (rule.is_limit_min and rule.limit_min>gauge_reads.value) or (rule.is_limit_max and rule.limit_max<gauge_reads.value):
            task = rule.task_id
            order_ids = self.search( 
                [('asset_id', '=', asset.id),
                ('state', 'not in', ('draft','cancel')),
                ('maintenance_type', '=', 'cbm'),
                ('task_id', '=', task.id)],
                limit=1, order='date_execution desc')
            if len(order_ids) > 0:
                date = order_ids[0].date_execution
                Do = 1.0*calendar.timegm(time.strptime(date, "%Y-%m-%d %H:%M:%S"))
                Dg = 1.0*calendar.timegm(time.strptime(gauge_reads.date, "%Y-%m-%d"))
                if Do>Dg: return True
            order_ids = self.search( 
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
                order = order_ids[0]
                values['parts_lines'] = parts_lines + [[2,line.id] for line in order.parts_lines]
                order.write(values)
                return True
            values['parts_lines'] = parts_lines
            self.create(values)
        return True


class mro_task(models.Model):
    _inherit = 'mro.task'

    MAINTENANCE_TYPE_SELECTION = [
        ('cm', 'Corrective'),
        ('pm', 'Preventive'),
        ('cbm', 'Predictive')
    ]

    maintenance_type = fields.Selection(MAINTENANCE_TYPE_SELECTION, 'Maintenance Type', required=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: