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
from openerp.osv import fields, osv


class mro_gauge(osv.osv):
    _name = 'mro.gauge'
    _description = 'Asset Gauges'

    READING_TYPE_SELECTION = [
        ('dir', 'Direct'),
        ('src', 'Gauge')
    ]

    STATE_SELECTION = [
        ('draft', 'Setup'),
        ('reading', 'Reading')
    ]

    def _get_lines(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for gauge in self.browse(cr, uid, ids, context=context):
            line_ids = self.pool.get('mro.gauge.line').search(cr, uid,[('gauge_id', '=', gauge.id)], limit=1)
            res[gauge.id] = line_ids
        return res
    
    _columns = {
        'name': fields.many2one('mro.pm.parameter', 'Gauge', ondelete='restrict', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'state': fields.selection(STATE_SELECTION, 'Status', readonly=True),
        'reading_type': fields.selection(READING_TYPE_SELECTION, 'Reading Type', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'gauge_line_ids': fields.one2many('mro.gauge.line', 'gauge_id', 'Gauges'),
        'view_line_ids': fields.function(_get_lines, relation="mro.gauge.line", method=True, type="one2many"),
        'new_value': fields.float('New value'),
        'date': fields.related('gauge_line_ids', 'date', type='date', string='Date'),
        'value': fields.related('gauge_line_ids', 'value', type='float', string='Value'),
        'gauge_uom': fields.related('name', 'parameter_uom', type='many2one', relation='product.uom', string='Unit of Measure', readonly=True),
        'asset_id': fields.many2one('asset.asset', 'Asset', ondelete='restrict'),
        'parent_gauge_id': fields.many2one('mro.gauge', 'Source Gauge', ondelete='restrict', readonly=True, states={'draft': [('readonly', False)]}),
        'parent_ratio_id': fields.many2one('mro.pm.meter.ratio', 'Ratio to Source', ondelete='restrict'),
    }

    _defaults = {
        'state': lambda *a: 'draft',
        'reading_type': lambda *a: 'dir',
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'gauge_uom': lambda self, cr, uid, c: self.pool.get('ir.model.data').get_object(cr, uid, 'product', 'product_uom_hour', context=c).id,
    }

    def create(self, cr, uid, vals, context=None):
        if not vals.get('asset_id',False): return
        gauge_id = super(mro_gauge, self).create(cr, uid, vals, context=context)
        values = {
            'date': vals.get('date',time.strftime('%Y-%m-%d')),
            'value': vals.get('value',0),
            'gauge_id': gauge_id,
        }
        self.pool.get('mro.gauge.line').create(cr, uid, values)
        return gauge_id

    def write(self, cr, uid, ids, vals, context=None):
        for gauge in self.browse(cr, uid, ids):
            if vals.get('new_value',False) and gauge.state == 'reading':
                if gauge.reading_type == 'dir':
                    vals.update({'value': vals['new_value']})
                    vals.update({'date': time.strftime('%Y-%m-%d')})
                    if gauge.date != time.strftime('%Y-%m-%d'):
                        self.pool.get('mro.gauge.line').create(cr, uid, {
                            'date': vals.get('date',time.strftime('%Y-%m-%d')),
                            'value': vals.get('new_value',0),
                            'gauge_id': gauge.id,
                            })
                    child_gauge_ids = self.search(cr, uid, [('parent_gauge_id', '=', gauge.id),('state', '=', 'reading')])
                    self.write(cr, uid, child_gauge_ids, {'new_value':vals['new_value']})
                elif gauge.reading_type == 'src':
                    if gauge.parent_ratio_id:
                        vals.update({'new_value': self.pool.get('mro.pm.meter.ratio').calculate(cr, uid, gauge.parent_ratio_id.id, vals['new_value'])})
                    if gauge.parent_gauge_id.reading_type == 'dir':
                        vals.update({'value': vals['new_value']})
                        vals.update({'date': time.strftime('%Y-%m-%d')})
                        if gauge.date != time.strftime('%Y-%m-%d'):
                            self.pool.get('mro.gauge.line').create(cr, uid, {
                                'date': vals.get('date',time.strftime('%Y-%m-%d')),
                                'value': vals.get('value',0),
                                'gauge_id': gauge.id,
                                })
                        vals.update({'new_value': vals.get('value',0)})
        return super(mro_gauge, self).write(cr, uid, ids, vals, context=context)

    def onchange_parameter(self, cr, uid, ids, parameter):
        value = {}
        if parameter:
            value['gauge_uom'] = self.pool.get('mro.pm.parameter').browse(cr, uid, parameter).parameter_uom.id
        return {'value': value}

    def onchange_value(self, cr, uid, ids, value):
        fields = {}
        fields['value'] = {'date': time.strftime('%Y-%m-%d')}
        fields['value'].update({'value': value})
        return fields

    def activate_gauge(self, cr, uid, ids, context=None):
        for gauge in self.browse(cr, uid, ids):
            fields = {'state': 'reading'}
            fields['new_value'] = gauge.value
            if gauge.reading_type != 'src': fields['parent_gauge_id'] = False
            self.write(cr, uid, ids, fields)
        return True


class mro_gauge_line(osv.osv):
    _name = 'mro.gauge.line'
    _description = 'History of Asset Gauge Reading'
    _columns = {
        'date': fields.date('Date', required=True),
        'value': fields.float('Reading Value', required=True),
        'gauge_id': fields.many2one('mro.gauge', 'Gauge', ondelete='restrict'),
    }

    _order = 'date desc'


class mro_cbm_rule(osv.osv):
    """
    Defines Predictive Maintenance rules.
    """
    _name = "mro.cbm.rule"
    _description = "Predictive Maintenance Rule"

    _columns = {
        'name': fields.char('Name', size=64),
        'active': fields.boolean('Active', help="If the active field is set to False, it will allow you to hide the PdM without removing it."),
        'category_id': fields.many2one('asset.category', 'Asset Category', ondelete='restrict', required=True),
        'parameter_id': fields.many2one('mro.pm.parameter', 'Parameter', ondelete='restrict', required=True),
        'parameter_uom': fields.related('parameter_id', 'parameter_uom', type='many2one', relation='product.uom', string='Unit of Measure'),
        'task_id': fields.many2one('mro.task', 'Task', ondelete='restrict', required=True),
        'limit_min': fields.float('Min Limit'),
        'limit_max': fields.float('Max Limit'),
        'is_limit_min': fields.boolean('Min Limit'),
        'is_limit_max': fields.boolean('Max Limit'),
    }

    _defaults = {
        'active': True,
    }

    def onchange_category(self, cr, uid, ids, task, category):
        value = {}
        if task and category and category != self.pool.get('mro.task').browse(cr, uid, task).category_id.id:
            value['task_id'] = False
        return {'value': value}

    def onchange_parameter(self, cr, uid, ids, parameter):
        value = {}
        if parameter:
            value['parameter_uom'] = self.pool.get('mro.pm.parameter').browse(cr, uid, parameter).parameter_uom.id
        return {'value': value}

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'mro.cbm.rule') or '/'
        return super(mro_cbm_rule, self).create(cr, uid, vals, context=context)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: