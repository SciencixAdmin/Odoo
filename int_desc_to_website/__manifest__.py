# -*- coding: utf-8 -*-
{
    'name': "Internal Description on Website",

    'summary': "Adding product internal description to website",

    'description': "Adding product internal description to website",

    'author': "odoo",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website','product'],

    # always loaded
    'data': [
        'views/templates.xml',
    ],
}