# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    manufacture_qty_count = fields.Float('Manufacture Quantity Count', compute='_compute_manufacture_qty', store=False, digits=dp.get_precision('Product Unit of Measure'))

    # manufacture_infinity = fields.Char('Infinity', default='∞')

    # action is dummy
    def action_manufacture_qty(self):
        pass

    def _compute_manufacture_qty_helper(self, product_id):
        d = {}

        def bom_traverse(root_product, d, parent_qty):
            # only consider one bom
            if root_product.bom_ids:
                for bom_line_id in root_product.bom_ids[0].bom_line_ids:

                    if bom_line_id.product_id not in d:
                        d[bom_line_id.product_id] = bom_line_id.product_qty * parent_qty
                    else:
                        d[bom_line_id.product_id] += bom_line_id.product_qty * parent_qty
                    bom_traverse(bom_line_id.product_id, d, bom_line_id.product_qty)

        if product_id.bom_ids:
            bom_traverse(product_id, d, 1)  # traverse to make one root
            # print(d)
            qty_lst = [(key.qty_available + key.manufacture_qty_count)/d[key] for key in d.keys() if key.type == 'product']
            return min(qty_lst) if qty_lst else 9999999999.0
        else:
            return 0.0

        # recursion: does not handle nested components
        # if product_id.bom_ids and product_id.bom_ids.mapped('bom_line_ids'):
        #     return min([self._compute_manufacture_qty_helper(bl.product_id)/bl.product_qty if bl.product_qty else 0 for bl in product_id.bom_ids.mapped('bom_line_ids')]) + product_id.qty_available
        # else:
        #     return product_id.qty_available

    def _compute_manufacture_qty(self):
        for product_tmpl_id in self:
            # need to subtract the qty_available
            # since previous recursion helper must include qty_available to compute recursive steps
            # product_tmpl_id.manufacture_qty_count = self._compute_manufacture_qty_helper(product_tmpl_id) - product_tmpl_id.qty_available
            if product_tmpl_id.type == 'product':
                product_tmpl_id.manufacture_qty_count = self._compute_manufacture_qty_helper(product_tmpl_id)
