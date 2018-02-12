# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2016 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'Assets & Finance',
    'version': '1.3',
    'summary': 'Integrate Asset and Accounting',
    'description': """
Integrate financial and maintenance asset management.
===========================

This module allows use the same Assets for maintenance and accounting purposes.
Keep one entity in one place for escape mistakes!
    """,
    'author': 'CodUP',
    'website': 'http://codup.com',
    'category': 'Industries',
    'sequence': 0,
    'depends': ['asset','account_asset'],
    'data': ['asset_view.xml'],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
