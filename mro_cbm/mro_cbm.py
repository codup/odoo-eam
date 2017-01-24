# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2015-2017 CodUP (<http://codup.com>).
#
##############################################################################

import time
from odoo import api, fields, models


class mro_gauge(models.Model):
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

    def _get_lines(self):
        for gauge in self:
            gauge.view_line_ids = self.env['mro.gauge.line'].search([('gauge_id', '=', gauge.id)], limit=1)

    name = fields.Many2one('mro.pm.parameter', 'Gauge', ondelete='restrict', required=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection(STATE_SELECTION, 'Status', readonly=True, default='draft')
    reading_type = fields.Selection(READING_TYPE_SELECTION, 'Reading Type', required=True, readonly=True, states={'draft': [('readonly', False)]}, default='dir')
    gauge_line_ids = fields.One2many('mro.gauge.line', 'gauge_id', 'Gauges')
    view_line_ids = fields.One2many('mro.gauge.line', compute='_get_lines')
    new_value = fields.Float('New value')
    date = fields.Date(related='gauge_line_ids.date', string='Date', default=time.strftime('%Y-%m-%d'))
    value = fields.Float(related='gauge_line_ids.value', string='Value')
    gauge_uom = fields.Many2one(related='name.parameter_uom', string='Unit of Measure', readonly=True)
    asset_id = fields.Many2one('asset.asset', 'Asset', ondelete='restrict')
    parent_gauge_id = fields.Many2one('mro.gauge', 'Source Gauge', ondelete='restrict', readonly=True, states={'draft': [('readonly', False)]})
    parent_ratio_id = fields.Many2one('mro.pm.meter.ratio', 'Ratio to Source', ondelete='restrict')

    @api.model
    def create(self, vals):
        if not vals.get('asset_id',False): return
        gauge_id = super(mro_gauge, self).create(vals)
        values = {
            'date': vals.get('date',time.strftime('%Y-%m-%d')),
            'value': vals.get('value',0),
            'gauge_id': gauge_id.id,
        }
        self.env['mro.gauge.line'].create(values)
        return gauge_id

    @api.multi
    def write(self, vals):
        for gauge in self:
            if vals.get('new_value',False) and gauge.state == 'reading':
                if gauge.reading_type == 'dir':
                    vals.update({'value': vals['new_value']})
                    vals.update({'date': time.strftime('%Y-%m-%d')})
                    if gauge.date != time.strftime('%Y-%m-%d'):
                        self.env['mro.gauge.line'].create({
                            'date': vals.get('date',time.strftime('%Y-%m-%d')),
                            'value': vals.get('new_value',0),
                            'gauge_id': gauge.id,
                            })
                    child_gauge_ids = self.search([('parent_gauge_id', '=', gauge.id),('state', '=', 'reading')])
                    child_gauge_ids.write({'new_value':vals['new_value']})
                elif gauge.reading_type == 'src':
                    if gauge.parent_ratio_id:
                        vals.update({'new_value': gauge.parent_ratio_id.calculate(vals['new_value'])})
                    if gauge.parent_gauge_id.reading_type == 'dir':
                        vals.update({'value': vals['new_value']})
                        vals.update({'date': time.strftime('%Y-%m-%d')})
                        if gauge.date != time.strftime('%Y-%m-%d'):
                            self.env['mro.gauge.line'].create({
                                'date': vals.get('date',time.strftime('%Y-%m-%d')),
                                'value': vals.get('value',0),
                                'gauge_id': gauge.id,
                                })
                        vals.update({'new_value': vals.get('value',0)})
        return super(mro_gauge, self).write(vals)

    @api.onchange('new_value')
    def onchange_value(self):
        self.date = time.strftime('%Y-%m-%d')
        self.value = self.new_value

    def activate_gauge(self):
        for gauge in self:
            fields = {'state': 'reading'}
            fields['new_value'] = gauge.value
            if gauge.reading_type != 'src': fields['parent_gauge_id'] = False
            self.write(fields)
        return True


class mro_gauge_line(models.Model):
    _name = 'mro.gauge.line'
    _description = 'History of Asset Gauge Reading'

    date = fields.Date('Date', required=True)
    value = fields.Float('Reading Value', required=True)
    gauge_id = fields.Many2one('mro.gauge', 'Gauge', ondelete='restrict')

    _order = 'date desc'


class mro_cbm_rule(models.Model):
    _name = "mro.cbm.rule"
    _description = "Predictive Maintenance Rule"

    name = fields.Char('Name', size=64)
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the PdM without removing it.", default=True)
    category_id = fields.Many2one('asset.category', 'Asset Category', ondelete='restrict', required=True)
    parameter_id = fields.Many2one('mro.pm.parameter', 'Parameter', ondelete='restrict', required=True)
    parameter_uom = fields.Many2one(related='parameter_id.parameter_uom', string='Unit of Measure')
    task_id = fields.Many2one('mro.task', 'Task', ondelete='restrict', required=True)
    limit_min = fields.Float('Min Limit')
    limit_max = fields.Float('Max Limit')
    is_limit_min = fields.Boolean('Min Limit')
    is_limit_max = fields.Boolean('Max Limit')

    @api.onchange('task_id','category_id')
    def onchange_category(self):
        if self.task_id and self.category_id and self.category_id.id != self.task_id.category_id.id:
            self.task_id = False

    @api.model
    def create(self, vals):
        if vals.get('name','/')=='/':
            vals['name'] = self.env['ir.sequence'].next_by_code('mro.cbm.rule') or '/'
        return super(mro_cbm_rule, self).create(vals)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: