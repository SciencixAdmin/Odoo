# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    print_label_bool = fields.Boolean(string='Print Label', default=False)

class StockPicking(models.Model):
	_inherit = 'stock.picking'

	print_label_bool = fields.Boolean(related='picking_type_id.print_label_bool')

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	oem = fields.Char(string='OEM')
