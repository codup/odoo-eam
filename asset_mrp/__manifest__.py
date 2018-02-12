# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2016 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'Assets & Manufacturing',
    'version': '1.3',
    'summary': 'Integrate Asset and Manufacturing',
    'description': """
Integrate manufacturing and maintenance asset management.
===========================

This module allows use the same Assets for manufacturing and maintenance purposes.
Integration take in account following assumption. In manufacturing,
Work Center can be simple logical entity, but also can reference
to equipment that is physical asset. Each physical asset must be maintenable, but
not each can be manufacturing equipment. So, when you create Work Center, you can
reference it to asset.
Keep one entity in one place for escape mistakes!
    """,
    'author': 'CodUP',
    'website': 'http://codup.com',
    'category': 'Industries',
    'sequence': 0,
    'depends': ['asset','mrp'],
    'demo': ['asset_demo.xml'],
    'data': [
        'security/ir.model.access.csv',
        'mrp_view.xml'
    ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
