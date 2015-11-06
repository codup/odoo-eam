# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-2015 CodUP (<http://codup.com>).
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
    'name': 'MRO PM',
    'version': '1.3',
    'summary': 'Asset Proactive Maintenance',
    'description': """
Manage Proactive Maintenance process in OpenERP
=====================================

Asset Maintenance, Repair and Operation.
Add support for Proactive Maintenance.

Main Features
-------------
    * Meter Management for Asset
    * Planning Maintenance Work Orders base on Meters
    * PM Rules for Assets by Tag

Required modules:
    * asset
    * mro
    """,
    'author': 'CodUP',
    'website': 'http://codup.com',
    'category': 'Enterprise Asset Management',
    'sequence': 0,
    'images': ['images/meter_interval.png','images/pm_rule.png','images/asset_meters.png','images/update_meters.png','images/meter_ratio.png'],
    'depends': ['mro'],
    'demo': ['mro_pm_demo.xml'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/replan_view.xml',
        'mro_pm_view.xml',
        'mro_pm_sequence.xml',
        'asset_view.xml',
    ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: