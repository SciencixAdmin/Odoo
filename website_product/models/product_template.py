# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools

class ProductTemplate(models.Model):
    _inherit = "product.template"

    website_notes = fields.Text('Website Notes', translate=True, help='Notes that will appear on the website product page')
