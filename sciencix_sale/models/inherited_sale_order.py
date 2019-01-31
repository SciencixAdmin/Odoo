# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import timedelta
from odoo import api, fields, models, _

class SaleOrder(models.Model):

    _inherit = ['sale.order']

    add_notes = fields.Text(string="Additional notes", store=True)
    cust_ref = fields.Char(string="Customer Ref", store=True)
    so_valid_date = fields.Datetime(compute="_get_valid_date",string="Proforma Valid Until",store=True)

    @api.depends('date_order')
    def _get_valid_date(self):
        for r in self:
            if r.date_order:
                origin_date = fields.Datetime.from_string(r.date_order)
                valid = origin_date + timedelta(days=14,seconds=-1)
                print("origin Date: " + str(r.date_order) + " Valid Date: " + str(valid))
                r.so_valid_date = valid
