# -*- coding: utf-8 -*-
{
    'name': "Sciencix: Sale/Invoice Report Mod",

    'summary': """
        Report modifaction for SO/PRO-INV/INV for Sciencix.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Odoo",
    'website': "http://www.odoo.com",
    'sequence': 200,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
        'report/inherited_sale_report_templates.xml',
        'report/inherited_invoice_report_templates.xml',
    ],

}
