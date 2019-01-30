# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class AccountInvoiceLine(models.Model):
    _inherit = ['account.invoice.line']

    inv_hs_code = fields.Char(compute="_compute_hs_origin", string="Schedule B Number")
    inv_origin_id = fields.Many2one('res.country',compute="_compute_hs_origin",string="Country of Origin")

    @api.multi
    @api.depends('product_id','sale_line_ids')
    def _compute_hs_origin(self):
        for line in self:
            if line.product_id:
                cur_code = line.product_id.hs_code
                cur_country = line.product_id.country_origin
                print("Account's HS code: " + str(line.product_id.hs_code))
                print("Account's Origin: " + str(line.product_id.country_origin))

                line.inv_hs_code = cur_code
                line.inv_origin_id = cur_country

class AccountInvoice(models.Model):
    _inherit = ['account.invoice']

    inv_picking_policy = fields.Selection([
        ('direct', 'Deliver each product when available'),
        ('one', 'Deliver all products at once')],
        compute="_compute_sale_fields", string="Shipping Policy", store=True)
    #inv_add_notes =  fields.Text(compute="_compute_sale_fields", string="Additional Notes", store=True)
    #inv_cust_ref = fields.Char(compute="_compute_sale_fields", string="Customer Ref", store=True)

    sale_order_id = fields.Many2one('sale.order',compute="_compute_origin_sale", string="Original Sale Order",store=True)
    inv_add_notes = fields.Text(related='sale_order_id.add_notes', string="Additional Notes", store=True)
    inv_cust_ref = fields.Char(related='sale_order_id.cust_ref', string="Customer Ref", store=True)
    # inv_picking_policy = fields.Selection([
    #     ('direct', 'Deliver each product when available'),
    #     ('one', 'Deliver all products at once')],
    #     related='sale_order_id.picking_policy', string="Shipping Policy", store=True)

    @api.multi
    @api.depends('invoice_line_ids','invoice_line_ids.sale_line_ids','invoice_line_ids.sale_line_ids.order_id')
    def _compute_origin_sale(self):
        for account in self:
            if account.invoice_line_ids:
                if account.invoice_line_ids[0].sale_line_ids:
                    cur_order = account.invoice_line_ids[0].sale_line_ids[0].order_id
                    print("original sale: " + str(cur_order))
                    account.sale_order_id = cur_order

    @api.multi
    @api.depends('invoice_line_ids','invoice_line_ids.sale_line_ids','invoice_line_ids.sale_line_ids.order_id')
    def _compute_sale_fields(self):
        for account in self:
            if account.invoice_line_ids:
                if account.invoice_line_ids[0].sale_line_ids:
                    cur_shipping = account.invoice_line_ids[0].sale_line_ids[0].order_id.picking_policy
                    print("Account's Cust: " + str(cur_shipping))
                    account.inv_picking_policy = cur_shipping
