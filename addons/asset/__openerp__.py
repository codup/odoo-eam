# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-2014 CodUP (<http://codup.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Assets',
    'version': '1.6',
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
    """,
    'author': 'CodUP',
    'website': 'http://codup.com',
    'category': 'Enterprise Asset Management',
    'sequence': 0,
    'images': ['images/assets.png'],
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
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: