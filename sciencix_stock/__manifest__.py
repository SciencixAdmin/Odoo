# -*- coding: utf-8 -*-
{
    'name': 'Sciencix: stock',
    'summary': 'Sciencix: Material Shortage Report',
    'description': """
    The sales people need to check if a product is available or not. The product that they are checking might not have any On Hand qty, but it might have all teh components that are needed to manufacture it.
    Hence we need a button called - "Manufacture Qty" on the product itself. This will display the quantity that can be manufactured (based on the availability of the components and BOM)
    Now, the BOM components can also be of type manufacture, so the report should drill down till the last product.
    A scheduled action can be created that updates the Manufacture Qty at a certain interval, if the dynamic update will slow down the system.""",
    'license': 'OEEL-1',
    'author': 'Odoo Inc',
    'version': '0.1',
    'depends': ['stock', 'mrp'],
    'data': [
        'views/product_template_views.xml',
        'views/stock_picking_views.xml',

    ],
}