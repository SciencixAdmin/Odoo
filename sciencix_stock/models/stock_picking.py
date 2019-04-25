# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    is_quality_alert = fields.Boolean(string="Quality Alert")


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_quality_alert = fields.Boolean(related="picking_type_id.is_quality_alert", string="Quality Alert")
    customer_reference = fields.Char(related="sale_id.cust_ref", sting="Customer Reference (2)")
    customer_account_number = fields.Char(related="sale_id.customer_account_no", string="Customer Account Number", help="This is the customer delivery a/c detail, When creating the SO, this should also be pulled from the contact form if the delivery method is selected.")
    welcome_materials = fields.Boolean(related="sale_id.welcome_materials", string="Welcome Materials")
    do_not_insure = fields.Boolean(related="sale_id.do_not_insure", string="Do Not Insure")
    duty_paid = fields.Boolean(related="sale_id.duty_paid", string="Duty Paid")
    incoterms = fields.Many2one(related="sale_id.incoterm", string="Incoterms")
    no_signature_required = fields.Boolean(related="sale_id.no_signature_required", string="No Signature Required")
    source_mo_product_id = fields.Many2one('product.product', 'Source MO Product', compute='_compute_source_mo_product_id')

    @api.multi
    @api.depends('group_id.name')
    def _compute_source_mo_product_id(self):
        for picking in self:
            origin_mo = self.env['mrp.production'].search([('name', '=', picking.group_id.name)], limit=1)
            picking.source_mo_product_id = origin_mo.product_id
