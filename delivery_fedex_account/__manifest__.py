# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Fedex Delivery: Bill My Account",
    'summary': "Web",
    'description': """
Fedex Delivery: Bill My Account
===============================
- Fedex bill my account functionality. The shipping charges will be ditectly charged into customer's specified Fedex account.
""",
    "author": "Odoo Inc",
    'website': "https://www.odoo.com",
    'category': 'Custom Development',
    'version': '0.1',
    'depends': ['delivery_fedex', 'website_sale_delivery'],
    'data': [
        'views/delivery_fedex_views.xml',
        'views/sale_views.xml',
        'views/stock_picking_views.xml',
        'views/templates.xml'
    ],
    'license': 'OEEL-1',
}