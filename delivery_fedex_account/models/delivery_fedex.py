# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, tools, _
from odoo.tools import pdf
from odoo.exceptions import UserError
from odoo.addons.delivery_fedex.models.fedex_request import FedexRequest
from odoo.addons.delivery_fedex.models.delivery_fedex import _convert_curr_iso_fdx, _convert_weight

_logger = logging.getLogger(__name__)


class FedexReq(FedexRequest):

    def shipping_charges_payment_by_recipient(self, shipping_charges_payment_account):
        self.RequestedShipment.ShippingChargesPayment.PaymentType = 'RECIPIENT'
        Payor = self.client.factory.create('Payor')
        Payor.ResponsibleParty.AccountNumber = shipping_charges_payment_account
        self.RequestedShipment.ShippingChargesPayment.Payor = Payor

    def duties_payment_by_recipient(self, responsible_party_country_code, responsible_account_number):
        self.RequestedShipment.CustomsClearanceDetail.DutiesPayment.PaymentType = 'RECIPIENT'
        Payor = self.client.factory.create('Payor')
        Payor.ResponsibleParty.Address.CountryCode = responsible_party_country_code
        Payor.ResponsibleParty.AccountNumber = responsible_account_number
        self.RequestedShipment.CustomsClearanceDetail.DutiesPayment.Payor = Payor


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    fedex_bill_my_account = fields.Boolean(string='Bill My Account', help="If checked, ecommerce users will be prompted their FEDEX account number\n"
                                                                        "and delivery fees will be charged on it.")

    def fedex_send_shipping(self, pickings):
        res = []

        for picking in pickings:

            srm = FedexReq(self.log_xml, request_type="shipping", prod_environment=self.prod_environment)

            superself = self.sudo()
            srm.web_authentication_detail(superself.fedex_developer_key, superself.fedex_developer_password)
            srm.client_detail(superself.fedex_account_number, superself.fedex_meter_number)

            srm.transaction_detail(picking.id)

            package_type = picking.package_ids and picking.package_ids[0].packaging_id.shipper_package_code or self.fedex_default_packaging_id.shipper_package_code
            srm.shipment_request(self.fedex_droppoff_type, self.fedex_service_type, package_type, self.fedex_weight_unit, self.fedex_saturday_delivery)
            srm.set_currency(_convert_curr_iso_fdx(picking.company_id.currency_id.name))
            srm.set_shipper(picking.company_id.partner_id, picking.picking_type_id.warehouse_id.partner_id)
            srm.set_recipient(picking.partner_id)
            # =============================================================================================
            #  CUSTOM CODE STARTS
            # =============================================================================================
            if self.fedex_bill_my_account and picking.fedex_carrier_account:
                srm.shipping_charges_payment_by_recipient(picking.fedex_carrier_account)
            else:
                srm.shipping_charges_payment(superself.fedex_account_number)
            # =============================================================================================
            # CUSTOM CODE ENDS
            # =============================================================================================

            srm.shipment_label('COMMON2D', self.fedex_label_file_type, self.fedex_label_stock_type, 'TOP_EDGE_OF_TEXT_FIRST', 'SHIPPING_LABEL_FIRST')

            order_currency = picking.sale_id.currency_id or picking.company_id.currency_id

            net_weight = _convert_weight(picking.shipping_weight, self.fedex_weight_unit)

            # Commodities for customs declaration (international shipping)
            if self.fedex_service_type in ['INTERNATIONAL_ECONOMY', 'INTERNATIONAL_PRIORITY'] or (picking.partner_id.country_id.code == 'IN' and picking.picking_type_id.warehouse_id.partner_id.country_id.code == 'IN'):

                commodity_currency = order_currency
                total_commodities_amount = 0.0
                commodity_country_of_manufacture = picking.picking_type_id.warehouse_id.partner_id.country_id.code

                for operation in picking.move_line_ids:
                    product_line = picking.sale_id.order_line.filtered(lambda x: x.product_id == operation.product_id)[0]
                    commodity_amount = product_line.price_subtotal / product_line.product_uom_qty
                    total_commodities_amount += (commodity_amount * operation.qty_done)
                    commodity_description = operation.product_id.name
                    commodity_number_of_piece = '1'
                    commodity_weight_units = self.fedex_weight_unit
                    commodity_weight_value = _convert_weight(operation.product_id.weight * operation.qty_done, self.fedex_weight_unit)
                    commodity_quantity = operation.qty_done
                    commodity_quantity_units = 'EA'
                    srm.commodities(_convert_curr_iso_fdx(commodity_currency.name), commodity_amount, commodity_number_of_piece, commodity_weight_units, commodity_weight_value, commodity_description, commodity_country_of_manufacture, commodity_quantity, commodity_quantity_units)
                srm.customs_value(_convert_curr_iso_fdx(commodity_currency.name), total_commodities_amount, "NON_DOCUMENTS")
                # =============================================================================================
                #  CUSTOM CODE STARTS
                # =============================================================================================
                if self.fedex_bill_my_account and picking.fedex_carrier_account:
                    srm.duties_payment_by_recipient(picking.picking_type_id.partner_id.country_id.code, picking.fedex_carrier_account)
                else:
                    srm.duties_payment(picking.picking_type_id.warehouse_id.partner_id.country_id.code, superself.fedex_account_number)
                # =============================================================================================
                #  CUSTOM CODE ENDS
                # =============================================================================================

            package_count = len(picking.package_ids) or 1

            # TODO RIM master: factorize the following crap

            ################
            # Multipackage #
            ################
            if package_count > 1:

                # Note: Fedex has a complex multi-piece shipping interface
                # - Each package has to be sent in a separate request
                # - First package is called "master" package and holds shipping-
                #   related information, including addresses, customs...
                # - Last package responses contains shipping price and code
                # - If a problem happens with a package, every previous package
                #   of the shipping has to be cancelled separately
                # (Why doing it in a simple way when the complex way exists??)

                master_tracking_id = False
                package_labels = []
                carrier_tracking_ref = ""

                for sequence, package in enumerate(picking.package_ids, start=1):

                    package_weight = _convert_weight(package.shipping_weight, self.fedex_weight_unit)
                    srm.add_package(package_weight, sequence_number=sequence)
                    srm.set_master_package(net_weight, package_count, master_tracking_id=master_tracking_id)
                    request = srm.process_shipment()
                    print(request)
                    package_name = package.name or sequence

                    warnings = request.get('warnings_message')
                    if warnings:
                        _logger.info(warnings)

                    # First package
                    if sequence == 1:
                        if not request.get('errors_message'):
                            master_tracking_id = request['master_tracking_id']
                            package_labels.append((package_name, srm.get_label()))
                            carrier_tracking_ref = request['tracking_number']
                        else:
                            raise UserError(request['errors_message'])

                    # Intermediary packages
                    elif sequence > 1 and sequence < package_count:
                        if not request.get('errors_message'):
                            package_labels.append((package_name, srm.get_label()))
                            carrier_tracking_ref = carrier_tracking_ref + "," + request['tracking_number']
                        else:
                            raise UserError(request['errors_message'])

                    # Last package
                    elif sequence == package_count:
                        # recuperer le label pdf
                        if not request.get('errors_message'):
                            package_labels.append((package_name, srm.get_label()))

                            if _convert_curr_iso_fdx(order_currency.name) in request['price']:
                                carrier_price = request['price'][_convert_curr_iso_fdx(order_currency.name)]
                            else:
                                _logger.info("Preferred currency has not been found in FedEx response")
                                company_currency = picking.company_id.currency_id
                                if _convert_curr_iso_fdx(company_currency.name) in request['price']:
                                    carrier_price = company_currency.compute(request['price'][_convert_curr_iso_fdx(company_currency.name)], order_currency)
                                else:
                                    carrier_price = company_currency.compute(request['price']['USD'], order_currency)

                            carrier_tracking_ref = carrier_tracking_ref + "," + request['tracking_number']

                            logmessage = _("Shipment created into Fedex<br/>"
                                           "<b>Tracking Numbers:</b> %s<br/>"
                                           "<b>Packages:</b> %s") % (carrier_tracking_ref, ','.join([pl[0] for pl in package_labels]))
                            if self.fedex_label_file_type != 'PDF':
                                attachments = [('LabelFedex-%s.%s' % (pl[0], self.fedex_label_file_type), pl[1]) for pl in package_labels]
                            if self.fedex_label_file_type == 'PDF':
                                attachments = [('LabelFedex.pdf', pdf.merge_pdf([pl[1] for pl in package_labels]))]
                            picking.message_post(body=logmessage, attachments=attachments)
                            shipping_data = {'exact_price': carrier_price,
                                             'tracking_number': carrier_tracking_ref}
                            res = res + [shipping_data]
                        else:
                            raise UserError(request['errors_message'])

            # TODO RIM handle if a package is not accepted (others should be deleted)

            ###############
            # One package #
            ###############
            elif package_count == 1:
                srm.add_package(net_weight)
                srm.set_master_package(net_weight, 1)

                # Ask the shipping to fedex
                request = srm.process_shipment()
                print(request)

                warnings = request.get('warnings_message')
                if warnings:
                    _logger.info(warnings)

                if not request.get('errors_message'):

                    if _convert_curr_iso_fdx(order_currency.name) in request['price']:
                        carrier_price = request['price'][_convert_curr_iso_fdx(order_currency.name)]
                    else:
                        _logger.info("Preferred currency has not been found in FedEx response")
                        company_currency = picking.company_id.currency_id
                        if _convert_curr_iso_fdx(company_currency.name) in request['price']:
                            carrier_price = company_currency.compute(request['price'][_convert_curr_iso_fdx(company_currency.name)], order_currency)
                        else:
                            carrier_price = company_currency.compute(request['price']['USD'], order_currency)

                    carrier_tracking_ref = request['tracking_number']
                    logmessage = (_("Shipment created into Fedex <br/> <b>Tracking Number : </b>%s") % (carrier_tracking_ref))

                    fedex_labels = [('LabelFedex-%s-%s.%s' % (carrier_tracking_ref, index, self.fedex_label_file_type), label)
                                    for index, label in enumerate(srm._get_labels(self.fedex_label_file_type))]
                    picking.message_post(body=logmessage, attachments=fedex_labels)

                    shipping_data = {'exact_price': carrier_price,
                                     'tracking_number': carrier_tracking_ref}
                    res = res + [shipping_data]
                else:
                    raise UserError(request['errors_message'])

            ##############
            # No package #
            ##############
            else:
                raise UserError(_('No packages for this picking'))

        return res
