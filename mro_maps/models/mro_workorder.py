# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2017 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models, _


class mro_order(models.Model):
    _inherit = 'mro.order'

    position = fields.Char('Map', related='asset_id.position')


class MroWorkOrder(models.Model):
    _inherit = 'mro.workorder'

    positions = fields.One2many('mro.order', 'wo_id', 'Maintenance Order')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: