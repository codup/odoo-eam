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

from openerp.osv import fields, osv

from openerp import tools

STATE_COLOR_SELECTION = [
    ('0', 'Red'),
    ('1', 'Green'),
    ('2', 'Blue'),
    ('3', 'Yellow'),
    ('4', 'Magenta'),
    ('5', 'Cyan'),
    ('6', 'Black'),
    ('7', 'White'),
    ('8', 'Orange'),
    ('9', 'SkyBlue')
]

class asset_state(osv.osv):
    """ 
    Model for asset states.
    """
    _name = 'asset.state'
    _description = 'State of Asset'
    _order = "sequence"

    STATE_SCOPE_TEAM = [
        ('0', 'Finance'),
        ('1', 'Warehouse'),
        ('2', 'Manufacture'),
        ('3', 'Maintenance'),
        ('4', 'Accounting')
    ]

    _columns = {
        'name': fields.char('State', size=64, required=True, translate=True),
        'sequence': fields.integer('Sequence', help="Used to order states."),
        'state_color': fields.selection(STATE_COLOR_SELECTION, 'State Color'),
        'team': fields.selection(STATE_SCOPE_TEAM, 'Scope Team'),
    }

    _defaults = {
        'sequence': 1,
    }
    
    def change_color(self, cr, uid, ids, context=None):
        state = self.browse(cr, uid, ids[0], context=context)
        color = int(state.state_color) + 1
        if (color>9): color = 0
        return self.write(cr, uid, ids, {'state_color': str(color)}, context=context)


class asset_category(osv.osv):
    _description = 'Asset Tags'
    _name = 'asset.category'
    _columns = {
        'name': fields.char('Tag', required=True, translate=True),
        'asset_ids': fields.many2many('asset.asset', id1='category_id', id2='asset_id', string='Assets'),
    }


class asset_asset(osv.osv):
    """
    Assets
    """
    _name = 'asset.asset'
    _description = 'Asset'
    _inherit = ['mail.thread']
    
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
        
    def _read_group_state_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None, team='3'):
        access_rights_uid = access_rights_uid or uid
        stage_obj = self.pool.get('asset.state')
        order = stage_obj._order
        # lame hack to allow reverting search, should just work in the trivial case
        if read_group_order == 'stage_id desc':
            order = "%s desc" % order
        # write the domain
        # - ('id', 'in', 'ids'): add columns that should be present
        # - OR ('team','=',team): add default columns that belongs team
        search_domain = []
        search_domain += ['|', ('team','=',team)]
        search_domain += [('id', 'in', ids)]
        stage_ids = stage_obj._search(cr, uid, search_domain, order=order, access_rights_uid=access_rights_uid, context=context)
        result = stage_obj.name_get(cr, access_rights_uid, stage_ids, context=context)
        # restore order of the search
        result.sort(lambda x,y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0])))
        return result, {}

    def _read_group_finance_state_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        return self._read_group_state_ids(cr, uid, ids, domain, read_group_order, access_rights_uid, context, '0')

    def _read_group_warehouse_state_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        return self._read_group_state_ids(cr, uid, ids, domain, read_group_order, access_rights_uid, context, '1')

    def _read_group_manufacture_state_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        return self._read_group_state_ids(cr, uid, ids, domain, read_group_order, access_rights_uid, context, '2')

    def _read_group_maintenance_state_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        return self._read_group_state_ids(cr, uid, ids, domain, read_group_order, access_rights_uid, context, '3')

    CRITICALITY_SELECTION = [
        ('0', 'General'),
        ('1', 'Important'),
        ('2', 'Very important'),
        ('3', 'Critical')
    ]

    _columns = {
        'name': fields.char('Asset Name', size=64, required=True, translate=True),
        'finance_state_id': fields.many2one('asset.state', 'State', domain=[('team','=','0')]),
        'warehouse_state_id': fields.many2one('asset.state', 'State', domain=[('team','=','1')]),
        'manufacture_state_id': fields.many2one('asset.state', 'State', domain=[('team','=','2')]),
        'maintenance_state_id': fields.many2one('asset.state', 'State', domain=[('team','=','3')]),
        'maintenance_state_color': fields.related('maintenance_state_id', 'state_color', type="selection", selection=STATE_COLOR_SELECTION, string="Color", readonly=True),
        'criticality': fields.selection(CRITICALITY_SELECTION, 'Criticality'),
        'property_stock_asset': fields.property(
          type='many2one',
          relation='stock.location',
          string="Asset Location",
          store=True,
          help="This location will be used as the destination location for installed parts during asset life."),
        'user_id': fields.many2one('res.users', 'Assigned to', track_visibility='onchange'),
        'active': fields.boolean('Active'),
        'asset_number': fields.char('Asset Number', size=64),
        'model': fields.char('Model', size=64),
        'serial': fields.char('Serial no.', size=64),
        'vendor_id':fields.many2one('res.partner', 'Vendor'),
        'manufacturer_id': fields.many2one('res.partner', 'Manufacturer'),
        'start_date': fields.date('Start Date'),
        'purchase_date': fields.date('Purchase Date'),
        'warranty_start_date': fields.date('Warranty Start'),
        'warranty_end_date': fields.date('Warranty End'),
        # image: all image fields are base64 encoded and PIL-supported
        'image': fields.binary("Image",
            help="This field holds the image used as image for the asset, limited to 1024x1024px."),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={
                'asset.asset': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized image of the asset. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved, "\
                 "only when the image exceeds one of those sizes. Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store={
                'asset.asset': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized image of the asset. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),
        'category_ids': fields.many2many('asset.category', id1='asset_id', id2='category_id', string='Tags'),
    }

    _defaults = {
        'active': True,
    }

    _group_by_full = {
        'finance_state_id': _read_group_finance_state_ids,
        'warehouse_state_id': _read_group_warehouse_state_ids,
        'manufacture_state_id': _read_group_manufacture_state_ids,
        'maintenance_state_id': _read_group_maintenance_state_ids,
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: