# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2017-2018 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models, _


class MroWorkOrder(models.Model):
    _name = 'mro.workorder'
    _description = 'Work Order'
    _inherit = ['mail.thread']

    STATE_SELECTION = [
        ('draft', 'Draft'),
        ('in_process', 'In Process'),
        ('done', 'Done')
    ]

    @api.depends('mo_ids')
    def _get_state(self):
        for order in self:
            state = 'undefined'
            for mo in order.mo_ids:
                if mo.state in ['released', 'ready']:
                    state = 'in_process'
                    break
                if mo.state in ['done', 'cancel'] and state in ['undefined', 'done']:
                    state = 'done'
                if mo.state == 'draft' and state in ['undefined', 'draft']:
                    state = 'draft'
            if state == 'undefined':
                state = 'draft'
            order.state = state

    name = fields.Char(
        'Work Order', copy=False, readonly=True, default=lambda x: _('New'))
    state = fields.Selection(STATE_SELECTION, 'Status', compute='_get_state')
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)]}, copy=False, default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self._uid)
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env['res.company']._company_default_get('mro.workorder'),
        required=True)
    mo_ids = fields.One2many('mro.order', 'wo_id', 'Maintenance Order')

    @api.model
    def create(self, values):
        if not values.get('name', False) or values['name'] == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('mro.workorder') or _('New')
        return super(MroWorkOrder, self).create(values)
