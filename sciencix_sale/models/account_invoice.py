# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    product_alias_id = fields.Many2one('product.alias', ondelete='set null', string='Product Alias', readonly=False)

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

