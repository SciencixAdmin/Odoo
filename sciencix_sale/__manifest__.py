# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sciencix: Sales Development',
    'summary': 'Sales Development',
    'sequence': 100,
    'license': 'OEEL-1',
    'website': 'https://www.odoo.com',
    'version': '1.0',
    'author': 'Odoo Inc',
    'description': """
Sales Development
=================
* Products: New field COO (Country of Origin) on product template, New field Schedule B Number on product template.
* Customer: This will be a drop-down list of all delivery methods, another field 'Customer Account number'. This is the customer delivery a/c detail
* sale order: above defined fields of Product and Customer auto-populate on Sale Order's Views
* report modification
    """,
    'category': 'Custom Development',
    'depends': ['sale_management', 'delivery', 'website_sale'],
    'data': [
        # views
        'views/product_views.xml',
        'views/partner_views.xml',
        'views/sale_order_views.xml',

        # Report
        'views/report_delivery_slip.xml',
        'views/report_sale_order.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
