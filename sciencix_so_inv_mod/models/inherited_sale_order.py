# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class SaleOrder(models.Model):

    _inherit = ['sale.order']

    add_notes = fields.Text(string="Additional notes", store=True)
    cust_ref = fields.Char(string="Customer Ref", store=True)
