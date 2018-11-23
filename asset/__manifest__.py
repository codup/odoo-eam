# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2018 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'Assets',
    'version': '1.12',
    'summary': 'Asset Management',
    'description': """
Managing Assets in Odoo.
===========================
Support following feature:
    * Location for Asset
    * Assign Asset to employee
    * Track warranty information
    * Custom states of Asset
    * States of Asset for different team: Finance, Warehouse, Manufacture, Maintenance and Accounting
    * Drag&Drop manage states of Asset
    * Asset Tags
    * Search by main fields
    """,
    'author': 'CodUP',
    'website': 'http://codup.com',
    'category': 'Industries',
    'sequence': 0,
    'depends': ['stock'],
    'demo': ['asset_demo.xml'],
    'data': [
        'security/asset_security.xml',
        'security/ir.model.access.csv',
        'asset_view.xml',
        'asset_data.xml',
        'stock_data.xml',
        'views/asset.xml',
    ],
    'installable': True,
    'application': True,
}
