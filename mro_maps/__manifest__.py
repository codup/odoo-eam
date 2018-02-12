# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2017 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'MRO Maps',
    'version': '0.1',
    'category': 'Industries',
    'summary': 'Show asset positions',
    'description': """
Show Asset on Map
==========================
Support following feature:
    * Asset positions in Work Order
    """,
    'author': 'CodUP',
    'license': 'AGPL-3',
    'website': 'http://codup.com',
    'sequence': 0,
    'depends': ['asset_map','mro','web_maps'],
    'data': [
        'views/mro_workorder_view.xml',
    ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
