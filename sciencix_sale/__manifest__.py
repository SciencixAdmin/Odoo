# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sciencix: Sales Development',
    'summary': 'Sales Development',
    'sequence': 100,
    'license': 'OEEL-1',
    'website': 'https://www.odoo.com',
    'version': '2.0',
    'author': 'Odoo Inc',
    'description': """
Sales Development
=================
* Products: New field COO (Country of Origin) on product template, New field Schedule B Number on product template.
* Customer: This will be a drop-down list of all delivery methods, another field 'Customer Account number'. This is the customer delivery a/c detail
* sale order: above defined fields of Product and Customer auto-populate on Sale Order's Views
* report modification
* Adding product notes to website"

Sales Development Part 2
========================
Various customers call the same product differently.
Let's say they have a product "ABC123" in the system.
Customer A calls it ProductA
Customer B calls it ProductB

So in the SO to Customer A, when we select product "ABC123", we should be able to select ProductA.

In the database create a Model called Alias. This model will have following fields - Alias name, product name and Customer.

Link this Alias to the Sale Order line. For Product "ABC123", I have 2 alias defined here [ProductA for CustomerA and ProductB for CustomerB].
When I create the SO for CustomerA and select product "ABC123", the system will display me the alias that I can choose for this product for the customer on the SO.
The alias that is selected in this SO should be printed in the SO report (additional column"Product" before the description column)
When I create the Invoice and Delivery Order, this Alias should pass on to the invoice and Delivery Order Form with the new added column.
Invoice Report and Delivery Slip report to have Product Column before Description
Slip report to have Product Column before Description
In the model "Alias" The product name is at the variant level.

Sales Development Part 3
========================
Various additions to the SO/PROFORMA-INVOICE/INVOICE reports.

Sales Development Part 4
========================
Various changes based on Task 1946626.

* Added fields to sale.order (migrated from studio fields, data needs to be moved to new fields):
    * Do Not Insure:            x_studio_field_oKpWY to do_not_insure
    * Welcome Materials:        x_studio_field_BYiHE to welcome_materials
    * Duty Paid:                x_studio_field_4jDfG to duty_paid
    * No Signature Required:    x_studio_field_aKJQw to no_signature_required

* Requirement 5: New report - Commercial Invoice
    * Create a new report printable from a sale order.
    * Duplicate the proforma Invoice report
    * Rename Proforma Invoice to Commercial Invoice
    * Remove the bank information block, Bank charge block and Please note block.
    * Add field Customer Reference (PO) from the SO under Other Information.
    """,
    'category': 'Custom Development',
    'depends': ['sale_management', 'delivery', 'website_sale', 'sale_stock', 'account'],
    'data': [
        # 'security/sciencix_sale.xml',
        'security/ir.model.access.csv',
        # views
        'views/product_alias.xml',
        'views/product_views.xml',
        'views/partner_views.xml',
        'views/sale_order_views.xml',
        'views/templates.xml',
        'views/account_invoice.xml',
        'views/stock_picking.xml',
        # Report
        # 'report/report_delivery_slip.xml',
        'report/report_sale_order.xml',
        # 'report/report_account_invoice.xml',
        'report/sale_report.xml',

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
