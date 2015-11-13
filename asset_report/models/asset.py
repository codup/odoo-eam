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

from openerp import api, models, fields


WORK_TIME = [
    ('0', 'Down Time'),
    ('1', 'Up Time')
]

class asset_state_history(models.Model):
    _name = 'asset.state.history'
    _description = 'History of Asset State'
    
    asset_id = fields.Many2one('asset.asset', 'Asset')
    maintenance_state_id = fields.Many2one('asset.state', 'State', domain=[('team','=','3')])


class asset_state(models.Model):
    _inherit = 'asset.state'

    work_time = fields.Selection(WORK_TIME, 'Work')


class asset_asset(models.Model):
    _inherit = 'asset.asset'

    @api.multi
    def write(self, vals):
        if vals.get('maintenance_state_id', False):
            for asset in self:
                self.env['asset.state.history'].create({
                    'maintenance_state_id': vals.get('maintenance_state_id', False),
                    'asset_id': asset.id
                    })
        return super(asset_asset, self).write(vals)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: