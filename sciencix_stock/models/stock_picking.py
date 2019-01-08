# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    is_quality_alert = fields.Boolean(string="Quality Alert")


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_quality_alert = fields.Boolean(related="picking_type_id.is_quality_alert", string="Quality Alert")
