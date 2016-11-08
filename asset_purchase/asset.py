# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2016 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models
from odoo.addons.asset.asset import STATE_COLOR_SELECTION


class asset_asset(models.Model):
    _inherit = 'asset.asset'

    finance_state_color = fields.Selection(related='finance_state_id.state_color', selection=STATE_COLOR_SELECTION, string="Color", readonly=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: