# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-2016 CodUP (<http://codup.com>).
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
    'name': 'MRO',
    'version': '1.4',
    'summary': 'Asset Maintenance, Repair and Operation',
    'description': """
Manage Maintenance process in OpenERP
=====================================

Asset Maintenance, Repair and Operation.
Support Breakdown Maintenance and Corrective Maintenance.

Main Features
-------------
    * Request Service/Maintenance Management
    * Maintenance Work Orders Management
    * Parts Management
    * Tasks Management (standard job)
    * Convert Maintenance Order to Task
    * Print Maintenance Order
    * Print Maintenance Request

Required modules:
    * asset
    """,
    'author': 'CodUP',
    'website': 'http://codup.com',
    'category': 'Industries',
    'sequence': 0,
    'depends': ['asset','purchase'],
    'demo': ['mro_demo.xml'],
    'data': [
        'security/mro_security.xml',
        'security/ir.model.access.csv',
        'wizard/reject_view.xml',
        'wizard/convert_order.xml',
        'asset_view.xml',
        'mro_workflow.xml',
        'mro_request_workflow.xml',
        'mro_sequence.xml',
        'mro_view.xml',
        'mro_report.xml',
        'mro_data.xml',
        'views/report_mro_order.xml',
        'views/report_mro_request.xml',
    ],
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: