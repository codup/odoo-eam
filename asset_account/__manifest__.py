# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2020 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'Assets & Finance',
    'version': '1.5',
    'summary': 'Integrate Asset and Accounting',
    'description': """
Integrate financial and maintenance asset management.
===========================

This module allows use the same Assets for maintenance and accounting purposes.
Keep one entity in one place for escape mistakes!
    """,
    'author': 'CodUP',
    'website': 'http://codup.com',
    'license': 'AGPL-3',
    'category': 'Industries',
    'sequence': 0,
    'depends': ['asset','account'],
    'data': ['views/account_view.xml'],
    'demo': ['demo/asset_demo.xml'],
    'installable': True,
}
