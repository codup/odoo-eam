# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2015-2016 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import models, fields

class asset_asset(models.Model):
    _inherit = 'asset.asset'
    
    name = fields.Char(track_visibility='onchange')
    finance_state_id = fields.Many2one(track_visibility='onchange')
    warehouse_state_id = fields.Many2one(track_visibility='onchange')
    manufacture_state_id = fields.Many2one(track_visibility='onchange')
    maintenance_state_id = fields.Many2one(track_visibility='onchange')
    maintenance_state_color = fields.Selection(track_visibility='onchange')
    criticality = fields.Selection(track_visibility='onchange')
    property_stock_asset = fields.Many2one(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')
    asset_number = fields.Char(track_visibility='onchange')
    model = fields.Char(track_visibility='onchange')
    serial = fields.Char(track_visibility='onchange')
    vendor_id = fields.Many2one(track_visibility='onchange')
    manufacturer_id = fields.Many2one(track_visibility='onchange')
    start_date = fields.Date(track_visibility='onchange')
    purchase_date = fields.Date(track_visibility='onchange')
    warranty_start_date = fields.Date(track_visibility='onchange')
    warranty_end_date = fields.Date(track_visibility='onchange')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: