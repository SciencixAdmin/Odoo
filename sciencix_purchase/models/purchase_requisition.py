# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class PurchaseRequisitionLine(models.Model):

    _inherit = "purchase.requisition.line"

    @api.multi
    @api.depends('product_id', 'requisition_id.vendor_id')
    def _compute_seller_product_code(self):
        for line in self:
            seller_product_code = line.product_id.default_code if line.product_id else ''
            if line.requisition_id and line.requisition_id.vendor_id and line.product_id:
                seller = line.product_id._select_seller(
                    partner_id=line.requisition_id.vendor_id,
                    quantity=line.product_qty,
                    date=line.requisition_id.date_order and line.requisition_id.date_order[:10],
                    uom_id=line.product_uom)
                if seller:
                    seller_product_code = seller.product_code
            line.seller_product_code = seller_product_code

    
    seller_product_code = fields.Char(compute='_compute_seller_product_code', string="Vendor Product Code")
    
