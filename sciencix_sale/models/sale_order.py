# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import timedelta
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    # already available "Delivery Method" on partner and sale order why they want added new field
    # default_delivery_carrier_id = fields.Many2one('delivery.carrier', string="Default Ship Method", help="When creating the SO for the customer, the default ship method should populate under 'Delivery Method' field")
    customer_account_no = fields.Char(string='Customer Account number', help="This is the customer delivery a/c detail, When creating the SO, this should also be pulled from the contact form if the delivery method is selected.")

    add_notes = fields.Text(string="Additional notes", store=True)
    cust_ref = fields.Char(string="Customer Reference (PO)", store=True)
    so_valid_date = fields.Datetime(compute="_get_valid_date",string="Proforma Valid Until",store=True)
    welcome_materials = fields.Boolean(string="Welcome Materials")
    do_not_insure = fields.Boolean(string="Do Not Insure")
    duty_paid = fields.Boolean(string="Duty Paid")
    incoterms = fields.Char(string="Incoterms")
    no_signature_required = fields.Boolean(string="No Signature Required")

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        if self.partner_id.property_delivery_carrier_id:
            self.customer_account_no = self.partner_id.customer_account_no
        self.order_line._onchange_product_alias_id()

    @api.depends('date_order')
    def _get_valid_date(self):
        for r in self:
            if r.date_order:
                origin_date = fields.Datetime.from_string(r.date_order)
                valid = origin_date + timedelta(days=14,seconds=-1)
                r.so_valid_date = valid

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    country_origin = fields.Many2one('res.country', related="product_id.country_origin", string="Country of Origin")
    hs_code = fields.Char("Schedule B Number", related="product_id.hs_code")

    product_alias_id = fields.Many2one('product.alias', ondelete='set null', string='Product Alias')

    @api.onchange('product_id', 'order_id')
    def _onchange_product_alias_id(self):
        for line in self:
            if line.product_id and line.order_id.partner_id:
                alias_ids = self.env['product.alias'].search([('product_id', '=', line.product_id.id), ('partner_id', '=', line.order_id.partner_id.id)])
                if alias_ids:
                    # to prevent endless loop
                    # not sure if odoo automatically handle this kind of onchange?
                    if not line.product_alias_id or line.product_alias_id.id != alias_ids[0].id:
                        line.product_alias_id = alias_ids[0]
                else:
                    line.product_alias_id = False

    @api.onchange('product_alias_id')
    def _onchange_product(self):
        for line in self:
            if line.product_alias_id and line.order_id.partner_id:
                product_id = line.product_alias_id.product_id
                if product_id:
                    # to prevent endless loop
                    # not sure if odoo automatically handle this kind of onchange?
                    if not line.product_id or line.product_id.id != product_id.id:
                        line.product_id = product_id
                else:
                    line.product_id = False
