# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    fedex_carrier_account = fields.Char(related='sale_id.fedex_carrier_account', string='Carrier Account')
    fedex_service_type = fields.Selection(related='sale_id.fedex_service_type', string="fedex Service Type")
