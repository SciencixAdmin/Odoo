# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _create_delivery_line(self, carrier, price_unit):
        if self.carrier_id.delivery_type == 'fedex' and self.fedex_bill_my_account and self.fedex_carrier_account:
            return True
        return super(SaleOrder, self)._create_delivery_line(carrier, price_unit)

    fedex_carrier_account = fields.Char(string='Carrier Account', copy=False)
    fedex_service_type = fields.Selection(related="carrier_id.fedex_service_type", string="Fedex Service Type")
    fedex_bill_my_account = fields.Boolean(related='carrier_id.fedex_bill_my_account', readonly=True)
