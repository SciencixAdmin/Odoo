# -*- coding: utf-8 -*-
{
    'name': 'Sciencix: stock',
    'summary': 'Sciencix: Stock Modifications',
    'description': """
This module contains the following changes to the stock module:

Material Shortage Report
========================

The sales people need to check if a product is available or not. The product that they are checking might not have any On Hand qty, but it might have all teh components that are needed to manufacture it.

Hence we need a button called - "Manufacture Qty" on the product itself. This will display the quantity that can be manufactured (based on the availability of the components and BOM)

Now, the BOM components can also be of type manufacture, so the report should drill down till the last product.

A scheduled action can be created that updates the Manufacture Qty at a certain interval, if the dynamic update will slow down the system.

Task 1946626
============

- Requirement 1: Add a custom char field called Cycle Code and add it to the Inventory Adjustment report
- Requirement 2: Add the fields "Revision" and "Notes" from the MO form to the Production Order report
- Requirement 3: Modifications to the Picking Operations report:

  1. Add Customer Account Number and Delivery Method from the transfer form.
  2. If source document has MO, then display the product to be manufactured from the MO.
  3. Notes: Print warning on picking from the res.partner record (Customer -> Internal Notes -> Warning on the Picking. (If there is a partner is present on the picking)
  4. Column for COO. Country of Origin on the product form.
  5. Add the following check boxes in the header section (fields are on the Transfer Form)

    - Welcome Materials checkbox
    - Do Not Insure checkbox
    - Duty Paid checkbox
    - No Signature Required checkbox
    - Incoterms

- Requirement 4: Modifications to the Delivery Slip report

  1. Add field Customer Reference (PO) field. This is the Customer Reference (2) field on the Transfer Form (display only if there is a value)
  2. Remove time from the date.
  3. Add Customer PO field from the Sale Order form (display only if there is a value)
  4. Add Incoterms (display only if there is a value)
  5. Add TIN/VAT from partner_id. Label should be TIN if US, VAT if not. (display only if there is a value)


Fields migrated from studio:
----------------------------

Legend:
~~~~~~~
- (V):      Displayed on views.
- (NM):     Needs data migration from old to new fields during deployment to production (the rest are related fields).
- (OOP):    Observed only on the production DB and not the staging DB.

Quotation (sale.order):
~~~~~~~~~~~~~~~~~~~~~~~
- Welcome Materials:        x_studio_field_BYiHE to welcome_materials (V) (NM)
- Do not insure:            x_studio_field_oKpWY to do_not_insure (V) (NM)
- Duty Paid:                x_studio_field_4jDfG to welcome_materials (V) (NM)
- Incoterms:                x_studio_field_r5B8l to incoterms (V) (NM) (OOP)
- No signature required:    x_studio_field_aKJQw to no_signature_required (V) (NM) (OOP)

Transfers (stock.picking):
~~~~~~~~~~~~~~~~~~~~~~~~~~
- Customer Account Number:  x_studio_field_Sxb6D to customer_account_number (V)
- Customer Reference (2):   x_studio_field_iMKfh to customer_reference (V)
- Welcome Materials:        x_studio_field_7eGMk to welcome_materials (V)
- Do not insure:            x_studio_field_EZsYJ to do_not_insure (V)
- Duty Paid:                x_studio_field_NodiT to duty_paid (V)
- Incoterms:                x_studio_field_jz4QO to incoterms (V) (OOP)
- No signature required:    x_studio_field_I5Qcu to no_signature_required (V) (OOP)

Production (mrp.production):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Revision:                 x_studio_field_T6Hg5 to revision (V)
- Production Notes:         x_studio_field_FALJO to notes (V)

Product Template (product.template):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Cycle Code:               x_studio_field_OCliB to cycle_code (V) (NM)
- Revision:                 x_studio_field_ZBoP5 to revision (V) (NM)

Inventory Line (stock.inventory.line):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Cycle Code:               x_studio_field_1uL0r to cycle_code (V)

Bill Of Materials (mrp.bom):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Notes:                    x_studio_field_kAepg to notes (NM)
    """,

    'license': 'OEEL-1',
    'author': 'Odoo Inc',
    'version': '0.1',
    'depends': ['stock', 'quality_mrp', 'sciencix_sale', 'delivery'],
    'data': [
        'views/mrp_production_views.xml',
        'views/product_template_views.xml',
        'views/product_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_inventory_views.xml',
        'views/delivery_view.xml',
        'report/report_stockinventory.xml',
        'report/report_deliveryslip.xml',
        'report/mrp_production_templates.xml',
        'report/report_stockpicking_operations.xml',
    ],
}
