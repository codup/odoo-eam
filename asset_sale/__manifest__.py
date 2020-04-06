# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2020 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'Assets & Sale',
    'version': '1.5',
    'summary': 'Integrate Asset and Sale',
    'description': """
Integrate Maintenance and Sale.
===========================

This module allows use the same Assets for sale and maintenance purposes.
Keep one entity in one place for escape mistakes!
    """,
    'author': 'CodUP',
    'website': 'http://codup.com',
    'license': 'AGPL-3',
    'category': 'Industries',
    'sequence': 0,
    'depends': ['sale_management','asset'],
    'demo': ['asset_demo.xml'],
    'data': [
        'security/ir.model.access.csv',
        'sale_view.xml'
    ],
    'installable': True,
}
