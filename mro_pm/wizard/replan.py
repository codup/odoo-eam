# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2018 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models


class mro_pm_replan(models.TransientModel):
    _name = 'mro.pm.replan'
    _description = 'Replan PM'

    def replan_pm(self):
        self.env['mro.order'].replan_pm()
        return {'type': 'ir.actions.act_window_close',}
