# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models



class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    seller_product_code = fields.Char(string="Seller Product Code")
    seller_product_name = fields.Char(string="Seller Product Name")

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        super(PurchaseOrderLine, self)._onchange_quantity()
        if not self.product_id:
            return

        seller_product_name = False
        seller_product_code = False
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order[:10],
            uom_id=self.product_uom)

        product_lang = self.product_id.with_context(
            lang=self.partner_id.lang,
            partner_id=self.partner_id.id,
        )
        seller_product_name = product_lang.display_name

        if seller:
            seller_product_code = seller.product_code
        else:
            # when qty is under min_qty on product seller the display_name still
            #  bring vendor code  although seller is not found. Customer wants so making is dummy
            # will not work in case of custom description but then we fall back to default_code
            if '[' in self.name and ']' in self.name:
                seller_product_code = self.name[self.name.index('[')+1: self.name.index(']')]

        self.seller_product_code = seller_product_code if seller_product_code else self.product_id.default_code
        self.seller_product_name = seller_product_name
