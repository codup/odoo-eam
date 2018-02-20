# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2016 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'Assets & Purchase',
    'version': '1.3',
    'summary': 'Integrate Asset and Purchase',
    'description': """
Integrate Maintenance and Purchase.
===========================

This module allows use the same Assets for purchase and maintenance purposes.
Keep one entity in one place for escape mistakes!
    """,
    'author': 'CodUP',
    'website': 'http://codup.com',
    'category': 'Industries',
    'sequence': 0,
    'depends': ['purchase','asset'],
    'demo': ['asset_demo.xml'],
    'data': [
        'security/ir.model.access.csv',
        'purchase_view.xml'
    ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
