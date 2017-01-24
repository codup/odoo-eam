# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2017 CodUP (<http://codup.com>).
#
##############################################################################

import math
import time
import calendar
from odoo import api, fields, models


class mro_pm_parameter(models.Model):
    _name = 'mro.pm.parameter'
    _description = 'Asset Parameters'

    def _get_default_uom_id(self):
        return self.env['ir.model.data'].get_object('product', 'product_uom_hour').id

    name = fields.Char('Parameter', size=64, required=True, translate=True)
    parameter_uom = fields.Many2one('product.uom', 'Unit of Measure', required=True, default=_get_default_uom_id)


class mro_pm_meter(models.Model):
    _name = 'mro.pm.meter'
    _description = 'Asset Meters'

    READING_TYPE_SELECTION = [
        ('inc', 'Increase'),
        ('dec', 'Decrease'),
        ('cng', 'Change'),
        ('src', 'Meter')
    ]

    STATE_SELECTION = [
        ('draft', 'Setup'),
        ('reset', 'Detached'),
        ('reading', 'Reading')
    ]

    def _get_utilization(self):
        for meter in self:
            Dn = 1.0*calendar.timegm(time.strptime(time.strftime('%Y-%m-%d',time.gmtime()),"%Y-%m-%d"))
            Da = Dn - 3600*24*meter.av_time
            meter_line_obj = self.env['mro.pm.meter.line']
            meter_line_ids = meter_line_obj.search([('meter_id', '=', meter.id),('date', '<=', time.strftime('%Y-%m-%d',time.gmtime(Da)))], limit=1, order='date desc')
            if not len(meter_line_ids):
                meter_line_ids = meter_line_obj.search([('meter_id', '=', meter.id),('date', '>', time.strftime('%Y-%m-%d',time.gmtime(Da)))], limit=1, order='date')
                if not len(meter_line_ids):
                    meter.utilization = meter.min_utilization
                    continue
            meter_line = meter_line_ids[0]
            Dci = 1.0*calendar.timegm(time.strptime(meter_line.date, "%Y-%m-%d"))
            Ci = meter_line.total_value
            number = 0
            Us = 0
            meter_line_ids = meter_line_obj.search([('meter_id', '=', meter.id),('date', '>',meter_line.date)], order='date')
            for meter_line in meter_line_ids:
                Dci1 = 1.0*calendar.timegm(time.strptime(meter_line.date, "%Y-%m-%d"))
                Ci1 = meter_line.total_value
                if Dci1 != Dci:
                    Us = Us + (3600*24*(Ci1 - Ci))/(Dci1 - Dci)
                    Dci = Dci1
                    Ci = Ci1
                    number += 1
            if number:
                U = Us/number
                if U<meter.min_utilization:
                    U = meter.min_utilization
            else:   U = meter.min_utilization
            meter.utilization = U

    def _get_lines(self):
        for meter in self:
            meter.view_line_ids = self.env['mro.pm.meter.line'].search([('meter_id', '=', meter.id)], limit=1)

    name = fields.Many2one('mro.pm.parameter', 'Meter', ondelete='restrict', required=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection(STATE_SELECTION, 'Status', readonly=True, default='draft')
    reading_type = fields.Selection(READING_TYPE_SELECTION, 'Reading Type', required=True, readonly=True, states={'draft': [('readonly', False)]}, default='inc')
    meter_line_ids = fields.One2many('mro.pm.meter.line', 'meter_id', 'Meters')
    view_line_ids = fields.One2many('mro.pm.meter.line', compute='_get_lines')
    new_value = fields.Float('New value')
    date = fields.Date(related='meter_line_ids.date', string='Date', default=time.strftime('%Y-%m-%d'))
    value = fields.Float(related='meter_line_ids.value', string='Value')
    total_value = fields.Float(related='meter_line_ids.total_value', string='Total Value')
    meter_uom = fields.Many2one(related='name.parameter_uom', string='Unit of Measure', readonly=True)
    asset_id = fields.Many2one('asset.asset', 'Asset', ondelete='restrict')
    parent_meter_id = fields.Many2one('mro.pm.meter', 'Source Meter', ondelete='restrict', readonly=True, states={'draft': [('readonly', False)]})
    parent_ratio_id = fields.Many2one('mro.pm.meter.ratio', 'Ratio to Source', ondelete='restrict')
    utilization = fields.Float(compute='_get_utilization', string='Utilization (per day)')
    min_utilization = fields.Float('Min Utilization (per day)', required=True, default=10)
    av_time = fields.Float('Averaging time (days)', required=True)

    def get_reading(self, date):
        D = 1.0*calendar.timegm(time.strptime(date, "%Y-%m-%d %H:%M:%S"))
        meter = self
        meter_line_obj = self.env['mro.pm.meter.line']
        prev_read = meter_line_obj.search([('meter_id', '=', meter.id),('date', '<=', date)], limit=1, order='date desc')
        next_read = meter_line_obj.search([('meter_id', '=', meter.id),('date', '>', date)], limit=2, order='date')
        if not len(prev_read):
            if len(next_read) == 2:
                D1 = 1.0*calendar.timegm(time.strptime(next_read[0].date, "%Y-%m-%d"))
                D2 = 1.0*calendar.timegm(time.strptime(next_read[1].date, "%Y-%m-%d"))
                C1 = next_read[0].total_value
                C2 = next_read[1].total_value
                value = C1 - (D1-D)*(C2-C1)/(D2-D1)
            else:
                D1 = 1.0*calendar.timegm(time.strptime(next_read[0].date, "%Y-%m-%d"))
                C1 = next_read[0].total_value
                value = C1 - (D1-D)*meter.utilization/(3600*24)
        elif not len(next_read):
            D1 = 1.0*calendar.timegm(time.strptime(prev_read[0].date, "%Y-%m-%d"))
            C1 = prev_read[0].total_value
            value = C1 + (D-D1)*meter.utilization/(3600*24)
        else:
            D1 = 1.0*calendar.timegm(time.strptime(prev_read[0].date, "%Y-%m-%d"))
            D2 = 1.0*calendar.timegm(time.strptime(next_read[0].date, "%Y-%m-%d"))
            C1 = prev_read[0].total_value
            C2 = next_read[0].total_value
            value = C1 + (D-D1)*(C2-C1)/(D2-D1)
        return value	              

    @api.model
    def create(self, vals):
        if not vals.get('asset_id',False): return
        meter_id = super(mro_pm_meter, self).create(vals)
        values = {
            'date': vals.get('date',time.strftime('%Y-%m-%d')),
            'value': vals.get('value',0),
            'total_value': vals.get('total_value',0),
            'meter_id': meter_id.id,
        }
        self.env['mro.pm.meter.line'].create(values)
        return meter_id

    @api.multi
    def write(self, vals):
        for meter in self:
            if vals.get('new_value',False) and meter.state == 'reading':
                if meter.reading_type == 'inc':
                    if meter.value < vals['new_value']:
                        total_value = meter.total_value + vals['new_value'] - meter.value
                        vals.update({'value': vals['new_value']})
                        vals.update({'total_value': total_value})
                        vals.update({'date': time.strftime('%Y-%m-%d')})
                        if meter.date != time.strftime('%Y-%m-%d'):
                            self.env['mro.pm.meter.line'].create({
                                'date': vals.get('date',time.strftime('%Y-%m-%d')),
                                'value': vals.get('new_value',0),
                                'total_value': vals.get('total_value',0),
                                'meter_id': meter.id,
                                })
                        child_meter_ids = self.search([('parent_meter_id', '=', meter.id),('state', '=', 'reading')])
                        child_meter_ids.write({'new_value':vals['new_value'] - meter.value})
                    else:
                        del vals['new_value']
                elif meter.reading_type == 'dec':
                    if meter.value > vals['new_value']:
                        total_value = meter.total_value - vals['new_value'] + meter.value
                        vals.update({'value': vals['new_value']})
                        vals.update({'total_value': total_value})
                        vals.update({'date': time.strftime('%Y-%m-%d')})
                        if meter.date != time.strftime('%Y-%m-%d'):
                            self.env['mro.pm.meter.line'].create({
                                'date': vals.get('date',time.strftime('%Y-%m-%d')),
                                'value': vals.get('new_value',0),
                                'total_value': vals.get('total_value',0),
                                'meter_id': meter.id,
                                })
                        child_meter_ids = self.search([('parent_meter_id', '=', meter.id),('state', '=', 'reading')])
                        child_meter_ids.write({'new_value':meter.value - vals['new_value']})
                    else:
                        del vals['new_value']
                elif meter.reading_type == 'cng':
                    total_value = meter.total_value + vals['new_value']
                    vals.update({'value': vals['new_value']})
                    vals.update({'total_value': total_value})
                    vals.update({'date': time.strftime('%Y-%m-%d')})
                    if meter.date != time.strftime('%Y-%m-%d'):
                        self.env['mro.pm.meter.line'].create({
                            'date': vals.get('date',time.strftime('%Y-%m-%d')),
                            'value': vals.get('new_value',0),
                            'total_value': vals.get('total_value',0),
                            'meter_id': meter.id,
                            })
                    child_meter_ids = self.search([('parent_meter_id', '=', meter.id),('state', '=', 'reading')])
                    child_meter_ids.write({'new_value':vals['new_value']})
                    vals.update({'new_value': 0})
                elif meter.reading_type == 'src':
                    if meter.parent_ratio_id:
                        vals.update({'new_value': meter.parent_ratio_id.calculate(vals['new_value'])})
                    if meter.parent_meter_id.reading_type == 'inc':
                        total_value = meter.total_value + vals['new_value']
                        vals.update({'value': vals['new_value'] + meter.value})
                        vals.update({'total_value': total_value})
                        vals.update({'date': time.strftime('%Y-%m-%d')})
                        if meter.date != time.strftime('%Y-%m-%d'):
                            self.env['mro.pm.meter.line'].create({
                                'date': vals.get('date',time.strftime('%Y-%m-%d')),
                                'value': vals.get('value',0),
                                'total_value': vals.get('total_value',0),
                                'meter_id': meter.id,
                                })
                        vals.update({'new_value': vals.get('value',0)})
                    elif meter.parent_meter_id.reading_type == 'dec':
                        total_value = meter.total_value + vals['new_value']
                        vals.update({'value': meter.value - vals['new_value']})
                        vals.update({'total_value': total_value})
                        vals.update({'date': time.strftime('%Y-%m-%d')})
                        if meter.date != time.strftime('%Y-%m-%d'):
                            self.env['mro.pm.meter.line'].create({
                                'date': vals.get('date',time.strftime('%Y-%m-%d')),
                                'value': vals.get('value',0),
                                'total_value': vals.get('total_value',0),
                                'meter_id': meter.id,
                                })
                        vals.update({'new_value': vals.get('value',0)})
                    elif meter.parent_meter_id.reading_type == 'cng':
                        total_value = meter.total_value + vals['new_value']
                        vals.update({'value': vals['new_value']})
                        vals.update({'total_value': total_value})
                        vals.update({'date': time.strftime('%Y-%m-%d')})
                        if meter.date != time.strftime('%Y-%m-%d'):
                            self.env['mro.pm.meter.line'].create({
                                'date': vals.get('date',time.strftime('%Y-%m-%d')),
                                'value': vals.get('value',0),
                                'total_value': vals.get('total_value',0),
                                'meter_id': meter.id,
                                })
                        vals.update({'new_value': 0})
        return super(mro_pm_meter, self).write(vals)

    @api.onchange('new_value')
    def onchange_value(self):
        new_date = time.strftime('%Y-%m-%d')
        for meter in self:
            if meter.state == 'reading':
                if meter.reading_type == 'inc':
                    if meter.value < meter.new_value:
                        meter.total_value = meter.total_value + meter.new_value - meter.value
                        meter.value = meter.new_value
                        meter.date = new_date
                    else:
                        meter.new_value = meter.value
                elif meter.reading_type == 'dec':
                    if meter.value > meter.new_value:
                        meter.total_value = meter.total_value - meter.new_value + meter.value
                        meter.value = meter.new_value
                        meter.date = new_date
                    else:
                        meter.new_value = meter.value
                else:
                    meter.total_value = meter.total_value + meter.new_value
                    meter.value = meter.new_value
                    meter.date = new_date
            else:
                meter.value = meter.new_value
                meter.date = new_date

    def activate_meter(self):
        for meter in self:
            fields = {'state': 'reading'}
            if meter.reading_type == 'cng':
                fields['new_value'] = 0
            else: 
                fields['new_value'] = meter.value
            if meter.reading_type != 'src': fields['parent_meter_id'] = False
            meter.write(fields)
        return True

    def reset_meter(self):
        self.write({'state': 'reset'})
        return True

    def run_meter(self):
        self.write({'state': 'reading'})
        return True


class mro_pm_meter_line(models.Model):
    _name = 'mro.pm.meter.line'
    _description = 'History of Asset Meter Reading'

    date = fields.Date('Date', required=True)
    value = fields.Float('Reading Value', required=True)
    total_value = fields.Float('Total Value', required=True)
    meter_id = fields.Many2one('mro.pm.meter', 'Meter', ondelete='restrict')

    _order = 'date desc'


class mro_pm_meter_ratio(models.Model):
    _name = 'mro.pm.meter.ratio'
    _description = 'Rules for Meter to Meter Ratio'

    ROUNDING_TYPE_SELECTION = [
        ('ceil', 'Ceiling'),
        ('floor', 'Floor'),
        ('round', 'Rounding')
    ]

    RATIO_TYPE_SELECTION = [
        ('bigger', 'Source Bigger'),
        ('smaller', 'Source Smaller')
    ]

    name = fields.Char('Name', size=64, required=True, translate=True)
    rounding_type = fields.Selection(ROUNDING_TYPE_SELECTION, 'Rounding Type', required=True, default='ceil')
    precision = fields.Float('Rounding Precision', default=1)
    ratio = fields.Float('Ratio', required=True, default=1)
    ratio_type = fields.Selection(RATIO_TYPE_SELECTION, 'Ratio Type', required=True, default='bigger')

    @api.onchange('precision')
    def onchange_precision(self):
        if self.precision < 0.01: self.precision = 0.01 #we can't view smaller value
        self.precision = 10**math.floor(math.log10(self.precision))

    def calculate(self, value):
        if not value:
            return value
        if self.ratio_type == 'bigger':
            value = value/self.ratio
        else:
            value = value*self.ratio
        if self.rounding_type == 'round':
            value = round(value / self.precision) * self.precision
        elif self.rounding_type == 'ceil':
            value = math.ceil(value / self.precision) * self.precision
        elif self.rounding_type == 'floor':
            value = math.floor(value / self.precision) * self.precision
        return value


class mro_pm_meter_interval(models.Model):
    _name = 'mro.pm.meter.interval'
    _description = 'Meter interval'

    def _get_name(self):
        for interval in self:
            if interval.interval_min == interval.interval_max: interval.name = str(interval.interval_min)
            else: interval.name = str(interval.interval_min) + ' - ' + str(interval.interval_max)

    name = fields.Char(compute='_get_name', string='Interval')
    interval_min = fields.Float('Min', required=True, default=0.01)
    interval_max = fields.Float('Max', required=True, default=0.01)

    @api.onchange('interval_min')
    def onchange_min(self):
        if self.interval_min < 0.01: self.interval_min = 0.01 #interval can't be 0
        if self.interval_min > self.interval_max: self.interval_max = self.interval_min

    @api.onchange('interval_max')
    def onchange_max(self):
        if self.interval_max < 0.01: self.interval_max = 0.01 #interval can't be 0
        if self.interval_min > self.interval_max: self.interval_min = self.interval_max


class mro_pm_rule(models.Model):
    _name = "mro.pm.rule"
    _description = "Preventive Maintenance Rule"

    name = fields.Char('Name', size=64)
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the PM without removing it.", default=True)
    category_id = fields.Many2one('asset.category', 'Asset Category', ondelete='restrict', required=True)
    parameter_id = fields.Many2one('mro.pm.parameter', 'Parameter', ondelete='restrict', required=True)
    parameter_uom = fields.Many2one(related='parameter_id.parameter_uom', string='Unit of Measure')
    horizon = fields.Float('Planning horizon (months)', digits=(12,0), required=True)
    pm_rules_line_ids = fields.One2many('mro.pm.rule.line', 'pm_rule_id', 'Tasks')

    @api.onchange('category_id')
    def onchange_category(self):
        self.pm_rules_line_ids = []

    @api.model
    def create(self, vals):
        if vals.get('name','/')=='/':
            vals['name'] = self.env['ir.sequence'].next_by_code('mro.pm.rule') or '/'
        return super(mro_pm_rule, self).create(vals)


class mro_pm_rule_line(models.Model):
    _name = 'mro.pm.rule.line'
    _description = 'Rule for Task'

    task_id = fields.Many2one('mro.task', 'Task', ondelete='restrict', required=True)
    meter_interval_id = fields.Many2one('mro.pm.meter.interval', 'Meter Interval', ondelete='restrict', required=True)
    pm_rule_id = fields.Many2one('mro.pm.rule', 'PM Rule', ondelete='restrict')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: