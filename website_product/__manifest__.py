# -*- coding: utf-8 -*-
{
    'name': "Website Product Notes",

    'summary': "Adding product notes to website",

    'description': "Adding product notes to website",

    'author': "odoo",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website_sale','product'],

    # always loaded
    'data': [
        'views/templates.xml',
        'views/product_views.xml',
    ],
}