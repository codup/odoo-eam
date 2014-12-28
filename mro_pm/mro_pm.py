# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 CodUP (<http://codup.com>).
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

import math
import time
import calendar
from openerp.osv import fields, osv


class mro_pm_parameter(osv.osv):
    _name = 'mro.pm.parameter'
    _description = 'Asset Parameters'

    _columns = {
        'name': fields.char('Parameter', size=64, required=True, translate=True),
        'parameter_uom': fields.many2one('product.uom', 'Unit of Measure', required=True),
    }

    _defaults = {
        'parameter_uom': lambda self, cr, uid, c: self.pool.get('ir.model.data').get_object(cr, uid, 'product', 'product_uom_hour', context=c).id,
    }


class mro_pm_meter(osv.osv):
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
    
    def _get_utilization(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for meter in self.browse(cr, uid, ids, context=context):
            Dn = 1.0*calendar.timegm(time.strptime(time.strftime('%Y-%m-%d',time.gmtime()),"%Y-%m-%d"))
            Da = Dn - 3600*24*meter.av_time
            meter_line_obj = self.pool.get('mro.pm.meter.line')
            meter_line_ids = meter_line_obj.search(cr, uid, [('meter_id', '=', meter.id),('date', '<=', time.strftime('%Y-%m-%d',time.gmtime(Da)))], limit=1, order='date desc')
            if not len(meter_line_ids):
                meter_line_ids = meter_line_obj.search(cr, uid, [('meter_id', '=', meter.id),('date', '>', time.strftime('%Y-%m-%d',time.gmtime(Da)))], limit=1, order='date')
                if not len(meter_line_ids):
                    res[meter.id] = meter.min_utilization
                    continue
            meter_line = meter_line_obj.browse(cr, uid, meter_line_ids[0])
            Dci = 1.0*calendar.timegm(time.strptime(meter_line.date, "%Y-%m-%d"))
            Ci = meter_line.total_value
            number = 0
            Us = 0
            meter_line_ids = meter_line_obj.search(cr, uid, [('meter_id', '=', meter.id),('date', '>',meter_line.date)], order='date')
            for meter_line in meter_line_obj.browse(cr, uid, meter_line_ids):
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
            res[meter.id] = U
        return res
        
    def _get_lines(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for meter in self.browse(cr, uid, ids, context=context):
            line_ids = self.pool.get('mro.pm.meter.line').search(cr, uid,[('meter_id', '=', meter.id)], limit=1)
            res[meter.id] = line_ids
        return res
    
    _columns = {
        'name': fields.char('Meter', size=64, required=True, translate=True),
        'state': fields.selection(STATE_SELECTION, 'Status', readonly=True),
        'reading_type': fields.selection(READING_TYPE_SELECTION, 'Reading Type', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'meter_line_ids': fields.one2many('mro.pm.meter.line', 'meter_id', 'Meters'),
        'view_line_ids': fields.function(_get_lines, relation="mro.pm.meter.line", method=True, type="one2many"),
        'new_value': fields.float('New value'),
        'date': fields.related('meter_line_ids', 'date', type='date', string='Date'),
        'value': fields.related('meter_line_ids', 'value', type='float', string='Value'),
        'total_value': fields.related('meter_line_ids', 'total_value', type='float', string='Total Value'),
        'meter_uom': fields.many2one('product.uom', 'Unit of Measure', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'asset_id': fields.many2one('asset.asset', 'Asset', ondelete='restrict'),
        'parent_meter_id': fields.many2one('mro.pm.meter', 'Source Meter', ondelete='restrict', readonly=True, states={'draft': [('readonly', False)]}),
        'parent_ratio_id': fields.many2one('mro.pm.meter.ratio', 'Ratio to Source', ondelete='restrict'),
        'utilization': fields.function(_get_utilization, method=True, string='Utilization (per day)'),
        'min_utilization': fields.float('Min Utilization (per day)', required=True),
        'av_time': fields.float('Averaging time (days)', required=True),
    }
    
    _defaults = {
        'state': lambda *a: 'draft',
        'reading_type': lambda *a: 'inc',
        'min_utilization': 10,
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'meter_uom': lambda self, cr, uid, c: self.pool.get('ir.model.data').get_object(cr, uid, 'product', 'product_uom_hour', context=c).id,
    }
    
    def get_reading(self, cr, uid, id, date, context=None):
        D = 1.0*calendar.timegm(time.strptime(date, "%Y-%m-%d %H:%M:%S"))
        meter = self.browse(cr, uid, id, context=context)
        meter_line_obj = self.pool.get('mro.pm.meter.line')
        prev_read = meter_line_obj.search(cr, uid, [('meter_id', '=', meter.id),('date', '<=', date)], limit=1, order='date desc')
        next_read = meter_line_obj.search(cr, uid, [('meter_id', '=', meter.id),('date', '>', date)], limit=2, order='date')
        if not len(prev_read):
            if len(next_read) == 2:
                reads = meter_line_obj.browse(cr, uid, next_read)
                D1 = 1.0*calendar.timegm(time.strptime(reads[0].date, "%Y-%m-%d"))
                D2 = 1.0*calendar.timegm(time.strptime(reads[1].date, "%Y-%m-%d"))
                C1 = reads[0].total_value
                C2 = reads[1].total_value
                value = C1 - (D1-D)*(C2-C1)/(D2-D1)
            else:
                reads = meter_line_obj.browse(cr, uid, next_read)
                D1 = 1.0*calendar.timegm(time.strptime(reads[0].date, "%Y-%m-%d"))
                C1 = reads[0].total_value
                value = C1 - (D1-D)*meter.utilization/(3600*24)
        elif not len(next_read):
            reads = meter_line_obj.browse(cr, uid, prev_read)
            D1 = 1.0*calendar.timegm(time.strptime(reads[0].date, "%Y-%m-%d"))
            C1 = reads[0].total_value
            value = C1 + (D-D1)*meter.utilization/(3600*24)
        else:
            reads = meter_line_obj.browse(cr, uid, [prev_read[0],next_read[0]])
            D1 = 1.0*calendar.timegm(time.strptime(reads[0].date, "%Y-%m-%d"))
            D2 = 1.0*calendar.timegm(time.strptime(reads[1].date, "%Y-%m-%d"))
            C1 = reads[0].total_value
            C2 = reads[1].total_value
            value = C1 + (D-D1)*(C2-C1)/(D2-D1)
        return value	              

    def create(self, cr, uid, vals, context=None):
        if not vals.get('asset_id',False): return
        meter_id = super(mro_pm_meter, self).create(cr, uid, vals, context=context)
        values = {
            'date': vals.get('date',time.strftime('%Y-%m-%d')),
            'value': vals.get('value',0),
            'total_value': vals.get('total_value',0),
            'meter_id': meter_id,
        }
        self.pool.get('mro.pm.meter.line').create(cr, uid, values)
        return meter_id
        
    def write(self, cr, uid, ids, vals, context=None):
        for meter in self.browse(cr, uid, ids):
            if vals.get('new_value',False) and meter.state == 'reading':
                if meter.reading_type == 'inc':
                    if meter.value < vals['new_value']:
                        total_value = meter.total_value + vals['new_value'] - meter.value
                        vals.update({'value': vals['new_value']})
                        vals.update({'total_value': total_value})
                        vals.update({'date': time.strftime('%Y-%m-%d')})
                        if meter.date != time.strftime('%Y-%m-%d'):
                            self.pool.get('mro.pm.meter.line').create(cr, uid, {
                                'date': vals.get('date',time.strftime('%Y-%m-%d')),
                                'value': vals.get('new_value',0),
                                'total_value': vals.get('total_value',0),
                                'meter_id': meter.id,
                                })
                        child_meter_ids = self.search(cr, uid, [('parent_meter_id', '=', meter.id),('state', '=', 'reading')])
                        self.write(cr, uid, child_meter_ids, {'new_value':vals['new_value'] - meter.value})
                    else:
                        del vals['new_value']
                elif meter.reading_type == 'dec':
                    if meter.value > vals['new_value']:
                        total_value = meter.total_value - vals['new_value'] + meter.value
                        vals.update({'value': vals['new_value']})
                        vals.update({'total_value': total_value})
                        vals.update({'date': time.strftime('%Y-%m-%d')})
                        if meter.date != time.strftime('%Y-%m-%d'):
                            self.pool.get('mro.pm.meter.line').create(cr, uid, {
                                'date': vals.get('date',time.strftime('%Y-%m-%d')),
                                'value': vals.get('new_value',0),
                                'total_value': vals.get('total_value',0),
                                'meter_id': meter.id,
                                })
                        child_meter_ids = self.search(cr, uid, [('parent_meter_id', '=', meter.id),('state', '=', 'reading')])
                        self.write(cr, uid, child_meter_ids, {'new_value':meter.value - vals['new_value']})
                    else:
                        del vals['new_value']
                elif meter.reading_type == 'cng':
                    total_value = meter.total_value + vals['new_value']
                    vals.update({'value': vals['new_value']})
                    vals.update({'total_value': total_value})
                    vals.update({'date': time.strftime('%Y-%m-%d')})
                    if meter.date != time.strftime('%Y-%m-%d'):
                        self.pool.get('mro.pm.meter.line').create(cr, uid, {
                            'date': vals.get('date',time.strftime('%Y-%m-%d')),
                            'value': vals.get('new_value',0),
                            'total_value': vals.get('total_value',0),
                            'meter_id': meter.id,
                            })
                    child_meter_ids = self.search(cr, uid, [('parent_meter_id', '=', meter.id),('state', '=', 'reading')])
                    self.write(cr, uid, child_meter_ids, {'new_value':vals['new_value']})
                    vals.update({'new_value': 0})
                elif meter.reading_type == 'src':
                    if meter.parent_ratio_id:
                        vals.update({'new_value': self.pool.get('mro.pm.meter.ratio').calculate(cr, uid, meter.parent_ratio_id.id, vals['new_value'])})
                    if meter.parent_meter_id.reading_type == 'inc':
                        total_value = meter.total_value + vals['new_value']
                        vals.update({'value': vals['new_value'] + meter.value})
                        vals.update({'total_value': total_value})
                        vals.update({'date': time.strftime('%Y-%m-%d')})
                        if meter.date != time.strftime('%Y-%m-%d'):
                            self.pool.get('mro.pm.meter.line').create(cr, uid, {
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
                            self.pool.get('mro.pm.meter.line').create(cr, uid, {
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
                            self.pool.get('mro.pm.meter.line').create(cr, uid, {
                                'date': vals.get('date',time.strftime('%Y-%m-%d')),
                                'value': vals.get('value',0),
                                'total_value': vals.get('total_value',0),
                                'meter_id': meter.id,
                                })
                        vals.update({'new_value': 0})
        return super(mro_pm_meter, self).write(cr, uid, ids, vals, context=context)
    
    def onchange_value(self, cr, uid, ids, value):
        """
        onchange handler of value.
        """
        fields = {}
        fields['value'] = {'date': time.strftime('%Y-%m-%d')}
        for meter in self.browse(cr, uid, ids):
            fields['value'].update({'value': value})
            if meter.state == 'reading':
                if meter.reading_type == 'inc':
                    if meter.value < value:
                        total_value = meter.total_value + value - meter.value
                        fields['value'].update({'total_value': total_value})
                    else:
                        fields['value'].update({'new_value': meter.value})
                        fields['value'].update({'value': meter.value})
                        fields['value'].update({'total_value': meter.total_value})
                        fields['value'].update({'date': meter.date})
                elif meter.reading_type == 'dec':
                    if meter.value > value:
                        total_value = meter.total_value - value + meter.value
                        fields['value'].update({'total_value': total_value})
                    else:
                        fields['value'].update({'new_value': meter.value})
                        fields['value'].update({'value': meter.value})
                        fields['value'].update({'total_value': meter.total_value})
                        fields['value'].update({'date': meter.date})
                else:
                    total_value = meter.total_value + value
                    fields['value'].update({'total_value': total_value})
        return fields

    def activate_meter(self, cr, uid, ids, context=None):
        """ Activate meter.
        @return: True
        """
        for meter in self.browse(cr, uid, ids):
            fields = {'state': 'reading'}
            if meter.reading_type == 'cng':
                fields['new_value'] = 0
            else: 
                fields['new_value'] = meter.value
            if meter.reading_type != 'src': fields['parent_meter_id'] = False
            self.write(cr, uid, ids, fields)
        return True
        
    def reset_meter(self, cr, uid, ids, context=None):
        """ Reset meter.
        @return: True
        """
        self.write(cr, uid, ids, {'state': 'reset'})
        return True
    
    def run_meter(self, cr, uid, ids, context=None):
        """ Reset meter.
        @return: True
        """
        self.write(cr, uid, ids, {'state': 'reading'})
        return True
        
    
class mro_pm_meter_line(osv.osv):
    _name = 'mro.pm.meter.line'
    _description = 'History of Asset Meter Reading'
    _columns = {
        'date': fields.date('Date', required=True),
        'value': fields.float('Reading Value', required=True),
        'total_value': fields.float('Total Value', required=True),
        'meter_id': fields.many2one('mro.pm.meter', 'Meter', ondelete='restrict'),
    }
    
    _order = 'date desc'
    
    
class mro_pm_meter_ratio(osv.osv):
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
    
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
        'rounding_type': fields.selection(ROUNDING_TYPE_SELECTION, 'Rounding Type', required=True),
        'precision': fields.float('Rounding Precision'),
        'ratio': fields.float('Ratio', required=True),
        'ratio_type': fields.selection(RATIO_TYPE_SELECTION, 'Ratio Type', required=True),
    }
    
    _defaults = {
        'rounding_type': lambda *a: 'ceil',
        'ratio_type': lambda *a: 'bigger',
        'precision': 1,
        'ratio': 1,
    }
    
    def onchange_precision(self, cr, uid, ids, precision):
        """
        onchange handler of precision.
        """
        if precision < 0.01: precision = 0.01 #we can't view smaller value
        return {'value': {'precision': 10**math.floor(math.log10(precision))}}
    
    def calculate(self, cr, uid, ratio_id, value):
        """ Calculate value according to ratio.
        @return: New value
        """
        if not ratio_id or not value:
            return value
        ratio = self.browse(cr, uid, ratio_id)
        if ratio.ratio_type == 'bigger':
            value = value/ratio.ratio
        else:
            value = value*ratio.ratio
        if ratio.rounding_type == 'round':
            value = round(value / ratio.precision) * ratio.precision
        elif ratio.rounding_type == 'ceil':
            value = math.ceil(value / ratio.precision) * ratio.precision
        elif ratio.rounding_type == 'floor':
            value = math.floor(value / ratio.precision) * ratio.precision
        return value
        
        
        
class mro_pm_meter_interval(osv.osv):
    _name = 'mro.pm.meter.interval'
    _description = 'Meter interval'
    
    def _get_name(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for interval in self.browse(cr, uid, ids, context=context):
            if interval.interval_min == interval.interval_max: res[interval.id] = str(interval.interval_min)
            else: res[interval.id] = str(interval.interval_min) + ' - ' + str(interval.interval_max)
        return res	

    _columns = {
        'name': fields.function(_get_name, method=True, type='char', string='Interval'),
        'interval_min': fields.float('Min', required=True),
        'interval_max': fields.float('Max', required=True),
    }
    
    _defaults = {
        'interval_min': 0.01,
        'interval_max': 0.01,
    }
    
    def onchange_min(self, cr, uid, ids, min, max):
        """
        onchange handler of min value.
        """
        if min < 0.01: min = 0.01 #interval can't be 0
        if min > max: max = min
        return {'value': {'interval_min': min,'interval_max': max,}}
    
    def onchange_max(self, cr, uid, ids, min, max):
        """
        onchange handler of max value.
        """
        if max < 0.01: max = 0.01 #interval can't be 0
        if min > max: min = max
        return {'value': {'interval_min': min,'interval_max': max,}}        

        
class mro_pm_rule(osv.osv):
    """
    Defines Preventive Maintenance rules.
    """
    _name = "mro.pm.rule"
    _description = "Preventive Maintenance Rule"

    _columns = {
        'name': fields.char('Name', size=64),
        'active': fields.boolean('Active', help="If the active field is set to False, it will allow you to hide the PM without removing it."),
        'asset_id': fields.many2one('asset.asset', 'Asset', ondelete='restrict', required=True),
        'meter_id': fields.many2one('mro.pm.meter', 'Meter', ondelete='restrict', required=True),
        'meter_uom': fields.related('meter_id', 'meter_uom', type='many2one', relation='product.uom', string='Unit of Measure'),
        'horizon': fields.float('Planning horizon (months)', digits=(12,0), required=True),
        'pm_rules_line_ids': fields.one2many('mro.pm.rule.line', 'pm_rule_id', 'Tasks'),
    }

    _defaults = {
        'active': True,
    }
    
    def onchange_asset(self, cr, uid, ids, rule_lines):
        """
        onchange handler of asset.
        """
        value = {}
        value['meter_id'] = False
        value['pm_rules_line_ids'] = [[2,line[1],line[2]] for line in rule_lines if line[0]]
        return {'value': value}
    
    def onchange_meter(self, cr, uid, ids, meter):
        """
        onchange handler of meter.
        """
        value = {}
        if meter:
            meter_uom = self.pool.get('mro.pm.meter').browse(cr, uid, meter).meter_uom.id
            value['meter_uom'] = meter_uom
        return {'value': value}
        
    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'mro.pm.rule') or '/'
        return super(mro_pm_rule, self).create(cr, uid, vals, context=context)
    
    
    
class mro_pm_rule_line(osv.osv):
    _name = 'mro.pm.rule.line'
    _description = 'Rule for Task'
    _columns = {
        'task_id': fields.many2one('mro.task', 'Task', ondelete='restrict', required=True),
        'meter_interval_id': fields.many2one('mro.pm.meter.interval', 'Meter Interval', ondelete='restrict', required=True),
        'pm_rule_id': fields.many2one('mro.pm.rule', 'PM Rule', ondelete='restrict'),
    }
    
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: