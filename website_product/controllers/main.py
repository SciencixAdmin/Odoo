# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values):
        domain = super(WebsiteSale, self)._get_search_domain(search, category, attrib_values)
        if search:
            domain = request.website.sale_product_domain()
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', '|', ('name', 'ilike', srch), ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch),
                    ('website_notes', 'ilike', srch)]
        return domain

    