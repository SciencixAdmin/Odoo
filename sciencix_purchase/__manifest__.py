# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sciencix: Purchase Development',
    'summary': 'Purchase Development',
    'sequence': 100,
    'license': 'OEEL-1',
    'website': 'https://www.odoo.com',
    'version': '1.1',
    'author': 'Odoo Inc',
    'description': """
Purchase Development
====================
* report Customization
* PO Report Modification-
* 1. Remove Sciencix Address below the Logo.
* 2. Change the header Purchase Order Confirmation# to Purchase Order No:
* 3. Trim time from Order Date and Date requested
* 4. Add Ship via and Shipping account from PO Form.
* 5. Separate Internal Reference from the description and add it to a new column called " Part ID"
* 6. Change Footer email address to ap@sciencix.com [right now it is sales@sciencix.com
* 7. Add terms to besides Your Order Reference

* Call for Tender Modification-
* 1. Remove the Sciencix address right below logo
* 2. Rename Call for Tenders to: Blanket Order No:
* 3. Add Ship to (sciencix adress that was under the logo)
* 4. Add Bill to (Invoice address on company contact)
* 5. Add Attn: Vendor Name (This is the vendor as per the PO) There will always be one Vendor.
* 6. Under products, add Order date (MM/DD/YYYY) Terms, Ship Via and Ship Acct [from the agrement]
* 7. From Products remove Description, product UoM and Schedule Date.
* 8. Remove Request for Quotation Details totally
* 9. Add Order Details -

* This will have the below columns -
* PO - Purchase Orders numbers created on the blanket order
* Part ID - Internal reference of the product [generaly there will be only one product in the PO, but if there are more than one products, then display all]
* Description - Description of the product without internal reference
* Schedule Date - [from PO line]
* QTY [from PO line]
* UoM [from PO line]
* Unit Price [from PO line]
* Total [Subtotal from PO line]
* 10. Then add subtotal, Tax and Order Total (refer mockup) - this is the sum of all the PO Lines.
* 11. Notes (Terms and conditions form Agreement go here)
    """,
    'category': 'Custom Development',
    'depends': ['purchase', 'purchase_requisition'],
    'data': [
        # Report
        'report/report_purchase.xml',
        'report/report_agreement.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
