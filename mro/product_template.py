# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2017 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models, tools, _


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = "product.template"

    @api.multi
    @api.depends('categ_id')
    def _check_category(self):
        parts_category = self.env.ref('mro.product_category_mro', raise_if_not_found=False)
        for product in self:
            product.isParts = product.categ_id.id == parts_category.id

    isParts = fields.Boolean(compute='_check_category', store=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: