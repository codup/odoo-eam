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

from openerp import models, fields

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