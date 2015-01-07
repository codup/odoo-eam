# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 CodUP (<http://codup.com>).
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
    'name': 'MRO CBM',
    'version': '1.0',
    'summary': 'Asset Predictive Maintenance',
    'description': """
Manage Predictive Maintenance process in OpenERP
=====================================

Asset Maintenance, Repair and Operation.
Add support for Condition Based Maintenance.

Main Features
-------------
    * Gauge Management for Asset
    * Planning Maintenance Work Orders base on Gauges

Required modules:
    * asset
    * mro
    * mro_pm
    """,
    'author': 'CodUP',
    'website': 'http://codup.com',
    'category': 'Enterprise Asset Management',
    'sequence': 0,
    'images': ['static/description/icon.png'],
    'depends': ['mro_pm'],
    'demo': ['mro_cbm_demo.xml'],
    'data': [
        'wizard/replan_view.xml',
        'mro_cbm_view.xml',
        'mro_cbm_sequence.xml',
        'asset_view.xml',
    ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: