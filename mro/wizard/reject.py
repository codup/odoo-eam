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
from openerp import netsvc

class mro_request_reject(osv.osv_memory):
    _name = 'mro.request.reject'
    _description = 'Reject Request'
    
    _columns = {
        'reject_reason': fields.text('Reject Reason', required=True),
    }
    
    def reject_request(self, cr, uid, ids, context=None):
        if 'active_id' in context:
            reject_reason=self.browse(cr,uid,ids)[0].reject_reason
            self.pool.get('mro.request').write(cr,uid,context['active_id'],{'reject_reason':reject_reason})
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(uid, 'mro.request', context['active_id'], 'button_reject', cr)
        return {'type': 'ir.actions.act_window_close',}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: