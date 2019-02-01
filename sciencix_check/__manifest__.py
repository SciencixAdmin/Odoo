# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Sciencix: Check Report Mod",

    'summary': """
        Check Report modifaction for Sciencix.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Odoo",
    'website': "http://www.odoo.com",
    'sequence': 200,

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['l10n_us_check_printing'],

    # always loaded
    'data': [
        'report/ckus_check_middle.xml',
    ],

}
