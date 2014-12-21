# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 CodUP (<http://codup.com>).
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

from openerp.osv import osv

class StockMove(osv.osv):
    _inherit = 'stock.move'

    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = super(StockMove, self).write(cr, uid, ids, vals, context=context)
        from openerp import workflow
        if vals.get('state') == 'assigned':
            moves = self.browse(cr, uid, ids, context=context)
            mro_obj = self.pool.get('mro.order')
            order_ids = mro_obj.search(cr, uid, [('procurement_group_id', 'in', [x.group_id.id for x in moves])])
            for order_id in order_ids:
                if mro_obj.test_ready(cr, uid, [order_id]):
                    workflow.trg_validate(uid, 'mro.order', order_id, 'parts_ready', cr)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: