# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2018 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def write(self, vals):
        res = super(StockMove, self).write(vals)
        # from odoo import workflow
        # if vals.get('state') == 'assigned':
            # mro_obj = self.env['mro.order']
            # order_ids = mro_obj.search([('procurement_group_id', 'in', [x.group_id.id for x in self])])
            # for order_id in order_ids:
                # if order_id.test_ready():
                    # workflow.trg_validate(self.env.user.id, 'mro.order', order_id.id, 'parts_ready', self.env.cr)
        return res
