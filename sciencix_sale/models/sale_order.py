# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # already available "Delivery Method" on partner and sale order why they want added new field
    # default_delivery_carrier_id = fields.Many2one('delivery.carrier', string="Default Ship Method", help="When creating the SO for the customer, the default ship method should populate under 'Delivery Method' field")
    customer_account_no = fields.Char(string='Customer Account number', help="This is the customer delivery a/c detail, When creating the SO, this should also be pulled from the contact form if the delivery method is selected.")

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        if self.partner_id.property_delivery_carrier_id:
            self.customer_account_no = self.partner_id.customer_account_no


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    country_origin = fields.Many2one('res.country', related="product_id.country_origin", string="Country of Origin")
    hs_code = fields.Char("Schedule B Number", related="product_id.hs_code")