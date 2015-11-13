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

from openerp import tools
from openerp import models, fields, api
from openerp.addons.asset_report.models.asset import WORK_TIME


class AssetStateLog(models.Model):
    _name = "asset.state.log"
    _description = "Asset State Logs"
    _auto = False
    _rec_name = 'date'

    asset_id = fields.Many2one('asset.asset', 'Asset', readonly=True)
    maintenance_state_id = fields.Many2one('asset.state', 'State', readonly=True)
    work_time = fields.Selection(WORK_TIME, 'Work', related='maintenance_state_id.work_time', readonly=True)
    duration = fields.Float('Duration(H)', readonly=True)
    date = fields.Datetime('Date', readonly=True)

    _order = 'asset_id, date desc'

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            SELECT id, asset_id, maintenance_state_id, create_date date,
            (EXTRACT(EPOCH FROM LEAD(create_date,1,now() at time zone 'utc') OVER (PARTITION BY asset_id ORDER BY create_date)) - EXTRACT(EPOCH FROM create_date))/3600 duration
            FROM asset_state_history
        )""" % (self._table))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: