# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2015-2016 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models


class asset_asset(models.Model):
    _inherit = 'asset.asset'

    gauge_ids = fields.One2many('mro.gauge', 'asset_id', 'Gauge')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: