# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp
import sys
from odoo.tools.profiler import profile
from odoo.tools.float_utils import float_round

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # manufacture_qty_count = fields.Float('Manufacture Quantity Count',  store=False, digits=dp.get_precision('Product Unit of Measure'))
    manufacture_qty_count_str = fields.Char('Manufacture Quantity Count', compute='_compute_manufacture_qty', store=False)

    # action is dummy
    def action_manufacture_qty(self):
        pass

    # in order to use _bom_find, product must be product.product object
    def _is_made_of_stockable(self, product):
        if product.type != 'product':
            return False
        else:
            bom_id = product.bom_ids._bom_find(product=product)  # find the right bom
            if not bom_id or not bom_id.bom_line_ids:
                return True
            else:
                return any([self._is_made_of_stockable(c) for c in bom_id.bom_line_ids.mapped('product_id')])

    # this func gives us how much in stock qty each product we need for 'product'
    def get_products_qty(self):
        self.ensure_one()
        product = self.product_variant_id
        def get_products_qty_helper(p, d):
            bom_id = p.bom_ids._bom_find(product=p)
            if not bom_id or not bom_id.bom_line_ids:
                return
            direct_components = bom_id.bom_line_ids.mapped('product_id')
            for component in direct_components:
                # we only care about products that have qty restrictions
                if self._is_made_of_stockable(component):
                    d[component] = component.qty_available
                    get_products_qty_helper(component, d)

        dic = {}
        get_products_qty_helper(product, dic)
        return dic

    # This function answers this question:
    # is it possible to make n product with products_qty (a dictionary that
    # holds all available qty for restriction components)?
    def can_make(self, product, n, products_qty):

        # if there is no components at all, we can't make any
        direct_components = []
        bom_id = product.bom_ids._bom_find(product=product)
        if bom_id and bom_id.bom_line_ids:
            # using explode() so that we get flattened qty - assuming uom is taken care of
            boms_done, lines_done = bom_id.explode(product, n)
            direct_components = {l.product_id: dic.get('qty') for l, dic in lines_done}
        if not direct_components:
            return False

        next_layers = []
        # we only care about restriction components
        # if a component is a consumable or it is only made of consumable, it won't even show up in products_qty:
        restriction_components = [c for c in direct_components.keys() if c in products_qty.keys()]

        for component in restriction_components:
            if products_qty[component] >= direct_components[component]:
                # if we have enough on hand
                products_qty[component] -= direct_components[component]
            else:
                # if there is possibility that it can be manufactured, then we calc this later
                next_layers.append((component, direct_components[component] - products_qty[component]))
                products_qty[component] = 0.0

        # now it's time to calc the next layer if there is any
        for c, need_n in next_layers:
            if not self.can_make(c, need_n, products_qty):
                return False

        return True

    # brute force count helper
    def compute_manufactury_qty_brute_force_helper(self, product, products_qty):
        count = 0
        while self.can_make(product, 1, products_qty):
            # print('made one {}'.format(product.name))
            count += 1
            # add an upper bound just in case
            if count >= sys.maxsize:
                break
        return count

    # this helper functions helps improve runtime when there are too much on hand components
    # could suck for deep layered boms tho
    def compute_manufactury_qty_optm_helper(self, product, products_qty, count, step):
        # base case
        if step < 1:
            return count

        # prepare for rollback
        products_qty_copy = products_qty.copy()

        if self.can_make(product, step, products_qty):
            return self.compute_manufactury_qty_optm_helper(product, products_qty, count + step, step * 2)
        else:
            return self.compute_manufactury_qty_optm_helper(product, products_qty_copy, count, step // 2)

    @profile
    def _compute_manufacture_qty(self):
        self.ensure_one()
        product = self.product_variant_id

        if not self._is_made_of_stockable(product):
            self.manufacture_qty_count_str = '∞'
        else:
            products_qty = self.get_products_qty()

            # test if the final result can be more than this threshold
            # if that is true, we want to call optmized helper
            threshold = 1000
            products_qty_copy = products_qty.copy()
            if not self.can_make(product, threshold, products_qty):
                final_result = self.compute_manufactury_qty_brute_force_helper(product, products_qty_copy)
            else:
                count, step = threshold, 1
                final_result = self.compute_manufactury_qty_optm_helper(product, products_qty, count, step)

            manufacture_qty = float_round(final_result, precision_rounding=product.uom_id.rounding)
            self.manufacture_qty_count_str = '{:.3f}'.format(manufacture_qty)
