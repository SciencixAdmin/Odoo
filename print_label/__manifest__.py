# -*- coding: utf-8 -*-
{
    'name': "Print Label",

    'summary': "Add barcode label on picking",

    'description': "Add barcode label on picking",

    'author': "Odoo",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock','product'],

    # always loaded
    'data': [
        'report/print_label.xml',
        'views/views.xml'
    ],
}
