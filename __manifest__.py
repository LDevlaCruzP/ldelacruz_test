# -*- coding: utf-8 -*-
{
    'name': "ldelacruz_test",

    'summary': "Ejercicios // desarrollador odoo",

    'description': """    """,

    'author': "Luis De la Cruz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'technical',
    'version': '17.0.0.2',
    'installable': True,
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'stock'],

    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "data/picking_mail_template_data.xml",
        "views/stock_picking_views.xml",
        "views/account_move_views.xml",
        "views/res_partner_views.xml",
        "views/new_report_stock_quant_views.xml",
        "wizard/wizard_send_topartner.xml",
        "wizard/account_move_reversal_view.xml",
    ],
}

