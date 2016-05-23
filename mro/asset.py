# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-2016 CodUP (<http://codup.com>).
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

from openerp.osv import fields, osv
from openerp.tools.translate import _


class asset_asset(osv.Model):
    _name = 'asset.asset'
    _inherit = 'asset.asset'

    def _mro_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict.fromkeys(ids, 0)
        maintenance = self.pool['mro.order']
        for asset in self.browse(cr, uid, ids, context=context):
            res[asset.id] = maintenance.search_count(cr,uid, [('asset_id', '=', asset.id)], context=context)
        return res

    def _next_maintenance(self, cr, uid, ids, field_name, arg, context=None):
        res = dict.fromkeys(ids, 0)
        maintenance = self.pool['mro.order']
        for asset in self.browse(cr, uid, ids, context=context):
            order_ids = maintenance.search(cr,uid,
                [('asset_id', '=', asset.id),
                ('state', 'not in', ('done','cancel'))],
                limit=1, order='date_execution')
            if len(order_ids) > 0:
                res[asset.id] = maintenance.browse(cr, uid, order_ids[0], context=context).date_execution
        return res

    _columns = {
        'mro_count': fields.function(_mro_count, string='# Maintenance', type='integer'),
        'maintenance_date': fields.function(_next_maintenance, string='Maintenance Date', type='date'),
    }

    def action_view_maintenance(self, cr, uid, ids, context=None):
        return {
            'domain': "[('asset_id','in',[" + ','.join(map(str, ids)) + "])]",
            'name': _('Maintenance Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'mro.order',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: