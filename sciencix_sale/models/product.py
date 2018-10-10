# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # IF the shipping address is outside United States.
    # Add a new field for Schedule B Number and display only if the COO is displayed.
    # If the country to where the order is being shipped is the United States then this column (COO)
    # and field Schedule B Number should not show up.
    country_origin = fields.Many2one('res.country', string="Country of Origin")
    # schedule_b_number = fields.Char("Schedule B Number")
