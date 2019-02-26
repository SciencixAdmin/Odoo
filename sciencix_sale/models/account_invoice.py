# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountInvoiceLine(models.Model):
    _inherit = ['account.invoice.line']

    product_alias_id = fields.Many2one('product.alias', ondelete='set null', string='Product Alias', readonly=False)

    inv_hs_code = fields.Char(compute="_compute_hs_origin", string="Schedule B Number")
    inv_origin_id = fields.Many2one('res.country',compute="_compute_hs_origin",string="Country of Origin")

    @api.model
    def create(self, vals):
        if vals.get('sale_line_ids', False):
            # print(vals.get('sale_line_ids'))
            sale_line_ids = self.env['sale.order.line'].search([('id', 'in', vals.get('sale_line_ids')[0][2])])
            product_alias_id = sale_line_ids[0].product_alias_id if sale_line_ids else False
            if product_alias_id:
                vals['product_alias_id'] = product_alias_id.id
        rid = super(AccountInvoiceLine, self).create(vals)
        return rid

    @api.onchange('product_id')
    def _onchange_product_alias_id(self):
        self.ensure_one()
        if self.product_id and self.invoice_id.partner_id:
            alias_ids = self.env['product.alias'].search(
                [('product_id', '=', self.product_id.id), ('partner_id', '=', self.invoice_id.partner_id.id)])
            if alias_ids:
                self.product_alias_id = alias_ids[0]
            else:
                self.product_alias_id = False

    @api.multi
    @api.depends('product_id','sale_line_ids')
    def _compute_hs_origin(self):
        for line in self:
            if line.product_id:
                cur_code = line.product_id.hs_code
                cur_country = line.product_id.country_origin

                line.inv_hs_code = cur_code
                line.inv_origin_id = cur_country

class AccountInvoice(models.Model):
    _inherit = ['account.invoice']

    inv_picking_policy = fields.Selection([
        ('direct', 'Deliver each product when available'),
        ('one', 'Deliver all products at once')],
        compute="_compute_sale_fields", string="Shipping Policy", store=True)

    sale_order_id = fields.Many2one('sale.order',compute="_compute_origin_sale", string="Original Sale Order",store=True)
    inv_add_notes = fields.Text(related='sale_order_id.add_notes', string="Additional Notes", store=True)
    inv_cust_ref = fields.Char(related='sale_order_id.cust_ref', string="Customer Ref", store=True)

    @api.multi
    @api.depends('invoice_line_ids','invoice_line_ids.sale_line_ids','invoice_line_ids.sale_line_ids.order_id')
    def _compute_origin_sale(self):
        for account in self:
            if account.invoice_line_ids:
                if account.invoice_line_ids[0].sale_line_ids:
                    cur_order = account.invoice_line_ids[0].sale_line_ids[0].order_id
                    account.sale_order_id = cur_order

    @api.multi
    @api.depends('invoice_line_ids','invoice_line_ids.sale_line_ids','invoice_line_ids.sale_line_ids.order_id')
    def _compute_sale_fields(self):
        for account in self:
            if account.invoice_line_ids:
                if account.invoice_line_ids[0].sale_line_ids:
                    cur_shipping = account.invoice_line_ids[0].sale_line_ids[0].order_id.picking_policy
                    account.inv_picking_policy = cur_shipping
