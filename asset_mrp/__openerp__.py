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
    'name': 'Assets & Manufacturing',
    'version': '1.2',
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