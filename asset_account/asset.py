# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2016 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models


class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    asset_id = fields.Many2one('asset.asset', 'Asset', required=True)

    @api.onchange('asset_id')
    def onchange_asset(self):
        self.name = self.asset_id.name
