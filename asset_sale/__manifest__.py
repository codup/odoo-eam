# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2016 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'Assets & Sale',
    'version': '1.3',
    'summary': 'Integrate Asset and Sale',
    'description': """
Integrate Maintenance and Sale.
===========================

This module allows use the same Assets for sale and maintenance purposes.
Keep one entity in one place for escape mistakes!
    """,
    'author': 'CodUP',
    'website': 'http://codup.com',
    'category': 'Industries',
    'sequence': 0,
    'depends': ['sale','asset'],
    'demo': ['asset_demo.xml'],
    'data': [
        'security/ir.model.access.csv',
        'sale_view.xml'
    ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
