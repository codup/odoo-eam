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

class account_asset(osv.osv):
    _inherit = 'account.asset.asset'
    
    def _get_name(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for asset in self.browse(cr, uid, ids, context=context):
            res[asset.id] = asset.asset_id.name
        return res	

    _columns = {
        'name': fields.function(_get_name, method=True, type='char', string='Asset'),
        'asset_id': fields.many2one('asset.asset', 'Asset', required=True, readonly=True, states={'draft':[('readonly',False)]}),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: