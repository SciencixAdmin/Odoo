# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'



    oem = fields.Char(string='OEM')
    # IF the shipping address is outside United States.
    # Add a new field for Schedule B Number and display only if the COO is displayed.
    # If the country to where the order is being shipped is the United States then this column (COO)
    # and field Schedule B Number should not show up.
    country_origin = fields.Many2one('res.country', string="Country of Origin")
    # schedule_b_number = fields.Char("Schedule B Number")
    website_notes = fields.Text('Website Notes', translate=True, help='Notes that will appear on the website product page')
    private = fields.Boolean()
    prod_partner_id = fields.Many2one('res.partner', string="Contact")
    prod_partner_ids = fields.Many2many(comodel_name='res.partner', relation="rel_prod_partner_ids_product", column1='product_tmpl_id', column2='partner_id', string="Contact")

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # Get Current User and Partner
        user = self.env['res.users'].browse(self.env.context.get('uid'))
        partner = user.partner_id
        if user.has_group('base.group_public') or user.has_group('base.group_portal'):
            # Domain added for checking whether product is private or not.
            # IF private then, check for partner and parent partner
            if partner:
                if partner.parent_id:
                    args.extend([
                        '|', ('private', '=', False),
                        '&', ('private', '=', True),
                        '|', ('prod_partner_ids', 'child_of', [partner.id]),
                             ('prod_partner_ids', 'parent_of', [partner.parent_id.id]),
                    ])
                else:
                    args.extend([
                        '|', ('private', '=', False),
                        '&', ('private', '=', True), ('prod_partner_ids', 'child_of', [partner.id])
                    ])
            else:
                args.extend([('private', '=', False)]) 
        return super(ProductTemplate, self).search(args, offset, limit, order, count=count)


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
