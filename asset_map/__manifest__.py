# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2017 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'Asset Map',
    'version': '0.1',
    'category': 'Industries',
    'summary': 'Show asset position',
    'description': """
Show Asset on Map
==========================
Support following feature:
    * Edit asset position
    """,
    'author': 'CodUP',
    'license': 'AGPL-3',
    'website': 'http://codup.com',
    'sequence': 0,
    'depends': ['asset','web_map'],
    'data': [
        'views/asset_view.xml',
    ],
    'demo': [
        'demo/asset_demo.xml',
    ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
