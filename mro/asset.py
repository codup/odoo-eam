# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2018 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models, _


class asset_asset(models.Model):
    _name = 'asset.asset'
    _inherit = 'asset.asset'

    def _mro_count(self):
        maintenance = self.env['mro.order']
        for asset in self:
            self.mro_count = maintenance.search_count([('asset_id', '=', asset.id)])

    def _next_maintenance(self):
        maintenance = self.env['mro.order']
        for asset in self:
            order_ids = maintenance.search(
                [('asset_id', '=', asset.id),
                ('state', 'not in', ('done','cancel'))],
                limit=1, order='date_execution')
            if len(order_ids) > 0:
                self.maintenance_date = order_ids[0].date_execution

    mro_count = fields.Integer(compute='_mro_count', string='# Maintenance')
    maintenance_date = fields.Datetime(compute='_next_maintenance', string='Maintenance Date')

    def action_view_maintenance(self):
        return {
            'domain': "[('asset_id','in',[" + ','.join(map(str, self.ids)) + "])]",
            'name': _('Maintenance Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'mro.order',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
