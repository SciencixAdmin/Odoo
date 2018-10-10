# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp
import sys

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    qty_produce = fields.Float('Manufacture Quantity', compute='_compute_manufacture_qty', 
                                digits=dp.get_precision('Product Unit of Measure'),)

    @api.multi
    @api.depends('bom_ids')
    def _compute_manufacture_qty(self):
        BOMOdel = self.env['mrp.bom']
        for pt in self:
            #find best matching bom using bom_find, behave same was routes
            bom_id = BOMOdel.with_context(company_id=self.company_id.id if self.company_id else False)._bom_find(product_tmpl=pt)
            pt.qty_produce = bom_id.qty_produce if bom_id else 0.0





