# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models



class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'
    
    seller_product_code = fields.Char(string="Seller Product Code")
    
    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        super(PurchaseOrderLine, self)._onchange_quantity()
        if not self.product_id:
            return

        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order[:10],
            uom_id=self.product_uom)

        self.seller_product_code = seller.product_code if seller else self.product_id.default_code