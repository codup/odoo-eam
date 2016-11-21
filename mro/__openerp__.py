# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2016 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'MRO',
    'version': '1.5',
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
        'mro_data.xml',
        'mro_view.xml',
        'mro_report.xml',
        'views/report_mro_order.xml',
        'views/report_mro_request.xml',
    ],
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: