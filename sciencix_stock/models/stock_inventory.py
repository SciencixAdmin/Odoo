# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    cycle_code = fields.Char(related="product_id.cycle_code", string="Cycle Code")
