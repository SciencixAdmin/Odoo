# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sciencix: Change Header Color',
    'version': '1.0',
    'category': 'Hidden',
    'sequence': 50,
    'summary': """Change Header Color""",
    'depends': ['web_enterprise', 'website_theme_install'],
    'description': """
* Change Header Color: #32CD32

""",
    'data': [
        'views/webclient_templates.xml',
    ],
    'license': 'OEEL-1',
    'installable': True,
    'auto_install': True,
}
