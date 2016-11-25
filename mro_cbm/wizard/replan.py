# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2015-2016 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models


class mro_cbm_replan(models.TransientModel):
    _name = 'mro.cbm.replan'
    _description = 'Replan PdM'

    def replan_cbm(self):
        self.env['mro.order'].replan_cbm()
        return {'type': 'ir.actions.act_window_close',}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: