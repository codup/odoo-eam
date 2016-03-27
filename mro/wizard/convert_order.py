# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-2016 CodUP (<http://codup.com>).
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

class mro_convert_order(osv.osv_memory):
    _name = 'mro.convert.order'
    _description = 'Convert Order to Task'

    def convert_order(self, cr, uid, ids, context=None):
        order_id = context.get('active_id', False)
        if order_id:
            order = self.pool.get('mro.order').browse(cr, uid, order_id)
            new_parts_lines = []
            for line in order.parts_lines:
                new_parts_lines.append([0,0,{
                    'name': line.name,
                    'parts_id': line.parts_id.id,
                    'parts_qty': line.parts_qty,
                    'parts_uom': line.parts_uom.id,
                    }])
            category_id = 1
            if order.asset_id.category_ids:
                for category in order.asset_id.category_ids:
                    category_id = category.id
                    break
            values = {
                'name': order.description,
                'category_id': category_id,
                'maintenance_type': order.maintenance_type if order.maintenance_type != 'bm' else 'cm',
                'parts_lines': new_parts_lines,
                'tools_description': order.tools_description,
                'labor_description': order.labor_description,
                'operations_description': order.operations_description,
                'documentation_description': order.documentation_description
            }
            return {
                'name': _('Task'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mro.task',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': self.pool.get('mro.task').create(cr, uid, values),
            }
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: