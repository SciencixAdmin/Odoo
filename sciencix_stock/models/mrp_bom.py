# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp

class MrpBom(models.Model):

    _inherit = 'mrp.bom'

    qty_produce = fields.Float('Can be produced', compute='_compute_bom_qty_produce', 
                                digits=dp.get_precision('Product Unit of Measure'),)

    def get_children(self, records, level=0):
        result = []

        def _get_rec(records, level):
            for l in records:
                result.append(l.product_id.id)
                if l.child_line_ids:
                    if level < 6:
                        level += 1
                    _get_rec(l.child_line_ids, level)
                    if level > 0 and level < 6:
                        level -= 1
            return result

        children = _get_rec(records, level)

        return children

    @api.multi
    def action_view_bom_struct_products(self):
        self.ensure_one()
        action = self.env.ref('product.product_normal_action').read()[0]
        childrens = self.get_children(self.bom_line_ids)
        action['domain'] = [('id', 'in', childrens)]
        return action


    @api.multi
    @api.depends('bom_line_ids', 'product_qty', 'product_uom_id')
    def _compute_bom_qty_produce(self):
        for bom in self:
            qunatities = []
            if bom.product_qty > 0.0:
                for line in bom.bom_line_ids:
                    qty_onhand = 0.0
                    qty_available = 0.0
                    if line.child_line_ids:
                        #find best matching bom using bom_find, behave same was routes
                        bom_id = self._bom_find(product=line.product_id)
                        if bom_id:
                            qty_onhand = bom_id.qty_produce
                    else:
                        qty_onhand = line.product_id.qty_available
                        #if BOMLine uom and prod. uom are not same then change qty_available to BOMline UOM 
                        if line.product_uom_id != line.product_id.uom_id:
                            qty_onhand = line.product_id.uom_id._compute_quantity(qty_onhand, line.product_uom_id)
                    if line.product_qty > 0.0:
                        qty_available = qty_onhand / line.product_qty
                    #adding if to save some call is qty is comes down to zero
                    if qty_available > 0.0:
                        #Note: Remove if it get's too expensive but this will round qty to bom line uom
                        qty_available = line.product_uom_id._compute_quantity(qty_available, line.product_uom_id)
                        qty_available = qty_available / bom.product_qty
                    qunatities.append(qty_available)
            bom.qty_produce = min(qunatities)