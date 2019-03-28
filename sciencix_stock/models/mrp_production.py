# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    is_quality_alert = fields.Boolean(related="picking_type_id.is_quality_alert", string="Quality Alert")
    revision = fields.Char(related="product_id.revision", string="Revision")
    notes = fields.Text(related="product_id.bom_ids.notes", string="Notes")
