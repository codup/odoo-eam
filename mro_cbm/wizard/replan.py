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

from openerp.osv import fields, osv

class mro_cbm_replan(osv.osv_memory):
    _name = 'mro.cbm.replan'
    _description = 'Replan PdM'
    
    def replan_cbm(self, cr, uid, ids, context=None):
        self.pool.get('mro.order').replan_cbm(cr, uid, context=context)
        return {'type': 'ir.actions.act_window_close',}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: