# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2016 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models
from odoo import netsvc

class mro_request_reject(models.TransientModel):
    _name = 'mro.request.reject'
    _description = 'Reject Request'

    reject_reason = fields.Text('Reject Reason', required=True)

    def reject_request(self):
        active_id = self._context.get('active_id')
        if active_id:
            request = self.env['mro.request'].browse(self._context.get('active_id'))
            request.write({'reject_reason':self.reject_reason})
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(self.env.user.id, 'mro.request', active_id, 'button_reject', self.env.cr)
        return {'type': 'ir.actions.act_window_close',}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: