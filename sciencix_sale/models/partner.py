# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # already available "Delivery Method" on partner and sale order why they want added new field
    # default_delivery_carrier_id = fields.Many2one('delivery.carrier', string="Default Ship Method", help="When creating the SO for the customer, the default ship method should populate under 'Delivery Method' field")
    customer_account_no = fields.Char(string='Customer Account number', help="This is the customer delivery a/c detail, When creating the SO, this should also be pulled from the contact form if the delivery method is selected.")
