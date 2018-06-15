# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2017-2018 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models, tools, _


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = "product.template"

    isParts = fields.Boolean('Can be Part')
