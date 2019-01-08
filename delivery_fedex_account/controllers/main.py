# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    @http.route("/shop/fedex_check_service_type", type='json', auth="public", website=True)
    def fedex_check_service_type_is_available(self, **post):
        return request.env['sale.order'].sudo().check_fedex_service_type(post)

    @http.route("/shop/fedex_carrier_account/set", type='http', auth="public", website=True)
    def set_fedex_carrier_account(self, **post):
        order = request.website.sale_get_order()
        # set fedex bill my account data in sale order
        if order.carrier_id.fedex_bill_my_account and post.get('fedex_carrier_account'):
            # Update Quotation with fedex_service_type and fedex_carrier_account
            order.write({
                'fedex_carrier_account': post['fedex_carrier_account']
            })
        return request.redirect("/shop/payment")

    @http.route("/shop/fedex_carrier_account/unset", type='http', auth="public", website=True)
    def reset_fedex_carrier_account(self, **post):
        order = request.website.sale_get_order()
        # remove fedex bill my account data in sale order
        if order.fedex_carrier_account:
            order.write({
                'fedex_carrier_account': False
            })
        return request.redirect("/shop/payment")
