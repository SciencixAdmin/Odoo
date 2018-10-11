# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # IF the shipping address is outside United States.
    # Add a new field for Schedule B Number and display only if the COO is displayed.
    # If the country to where the order is being shipped is the United States then this column (COO)
    # and field Schedule B Number should not show up.
    country_origin = fields.Many2one('res.country', string="Country of Origin")
    # schedule_b_number = fields.Char("Schedule B Number")
    website_notes = fields.Text('Website Notes', translate=True, help='Notes that will appear on the website product page')


class ProductAlias(models.Model):
    _name = 'product.alias'

    name = fields.Char('Alias')
    product_id = fields.Many2one('product.product', ondelete='set null', string='Product')
    partner_id = fields.Many2one('res.partner', ondelete='set null', string='Customer')

    _sql_constraints = [
        ('alias_uniq', 'UNIQUE(product_id, partner_id)',  _('Cannot create multiple alias for the same customer and the same product.')),
    ]


class ProductProduct(models.Model):
    _inherit = 'product.product'

    alias_ids = fields.One2many('product.alias', 'product_id', string='Alias')
