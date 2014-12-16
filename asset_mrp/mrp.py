# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-2014 CodUP (<http://codup.com>).
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

class mrp_workcenter(osv.osv):
    _inherit = 'mrp.workcenter'
    _columns = {
        'asset_ids': fields.many2many('asset.asset', string='Asset'),
    }


class mrp_bom(osv.osv):
    _inherit = 'mrp.bom'

    def _get_assets(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for bom in self.browse(cr, uid, ids, context=context):
            line_ids = []
            if bom.routing_id:
                for work_center in bom.routing_id.workcenter_lines:
                    line_ids += [asset.id for asset in work_center.workcenter_id.asset_ids]
            res[bom.id] = line_ids
        return res

    _columns = {
        'asset_ids': fields.function(_get_assets, relation="asset.asset", method=True, type="one2many"),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: