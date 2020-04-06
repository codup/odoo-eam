# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2020 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models


class mrp_workcenter(models.Model):
    _inherit = 'mrp.workcenter'

    asset_ids = fields.Many2many('asset.asset', string='Asset')


class mrp_bom(models.Model):
    _inherit = 'mrp.bom'

    @api.depends('routing_id')
    def _get_assets(self):
        for bom in self:
            line_ids = self.env['asset.asset']
            if bom.routing_id:
                for work_center in bom.routing_id.operation_ids:
                    line_ids |= work_center.workcenter_id.asset_ids
            bom.asset_ids = line_ids

    asset_ids = fields.One2many('asset.asset', compute='_get_assets')
