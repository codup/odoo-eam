# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2018 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models, _


class asset_asset(models.Model):
    _inherit = 'asset.asset'

    meter_ids = fields.One2many('mro.pm.meter', 'asset_id', 'Meter')

    def action_view_rules(self):
        category_ids = []
        for asset in self:
            category_ids = category_ids + [category.id for category in asset.category_ids]
        return {
            'domain': "[('category_id','in',[" + ','.join(map(str, category_ids)) + "])]",
            'name': _('Scheduling Rules'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'mro.pm.rule',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
