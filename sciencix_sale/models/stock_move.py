# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_alias_id = fields.Many2one('product.alias', ondelete='set null', readonly=True)

    @api.onchange('product_id')
    def _onchange_product_alias_id(self):
        self.ensure_one()
        if self.product_id and self.picking_id.partner_id:
            # print('yooooooooooo onchange')
            alias_ids = self.env['product.alias'].search(
                [('product_id', '=', self.product_id.id), ('partner_id', '=', self.picking_id.partner_id.id)])
            if alias_ids:
                # print(alias_ids)
                self.product_alias_id = alias_ids[0]
            else:
                # print('no alias')
                self.product_alias_id = False

    @api.model
    def create(self, vals):
        if vals.get('sale_line_id', False):
            sale_line_ids = self.env['sale.order.line'].search([('id', '=', vals.get('sale_line_id'))])
            product_alias_id = sale_line_ids[0].product_alias_id if sale_line_ids else False
            if product_alias_id:
                vals['product_alias_id'] = product_alias_id.id
        rid = super(StockMove, self).create(vals)
        if not rid.product_alias_id and rid.product_id and rid.picking_id and rid.picking_id.partner_id:
            alias_ids = self.env['product.alias'].search(
                [('product_id', '=', rid.product_id.id), ('partner_id', '=', rid.picking_id.partner_id.id)])
            rid.product_alias_id = alias_ids[0] if alias_ids else False
        return rid


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_alias_id = fields.Many2one('product.alias', ondelete='set null', related='move_id.product_alias_id', readonly=True)