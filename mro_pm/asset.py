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

from openerp.osv import fields, osv
from openerp.tools.translate import _


class asset_asset(osv.osv):
    _inherit = 'asset.asset'
    _columns = {
        'meter_ids': fields.one2many('mro.pm.meter', 'asset_id', 'Meter'),
    }

    def action_view_rules(self, cr, uid, ids, context=None):
        return {
            'domain': "[('asset_id','in',[" + ','.join(map(str, ids)) + "])]",
            'name': _('Scheduling Rules'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'mro.pm.rule',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: