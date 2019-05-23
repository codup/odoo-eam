# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2019 CodUP (<http://codup.com>).
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
            request.action_reject()
        return {'type': 'ir.actions.act_window_close',}
