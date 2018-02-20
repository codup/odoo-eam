# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2015-2016 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'MRO CBM',
    'version': '1.2',
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
    * PdM Rules for Assets by Tag

Required modules:
    * asset
    * mro
    * mro_pm
    """,
    'author': 'CodUP',
    'website': 'http://codup.com',
    'category': 'Industries',
    'sequence': 0,
    'depends': ['mro_pm'],
    'demo': ['mro_cbm_demo.xml'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/replan_view.xml',
        'mro_cbm_view.xml',
        'mro_cbm_sequence.xml',
        'asset_view.xml',
    ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
