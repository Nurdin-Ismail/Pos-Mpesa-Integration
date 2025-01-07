# -*- coding: utf-8 -*-
{

    'name': "Pos Mpesa Integration",
    'summary': "This module integrates MPesa with Odoo POS for seamless mobile payments, tracking transactions, and real-time updates",
    'description': 'Integrate MPesa payments with POS',
    'category': 'Point of Sale',

    'author': 'nur',
    'website': '',

    'category': 'Point of Sale',
    'version': '17.0.0.1.1',
    'depends': ['base','point_of_sale'],

    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'pos_mpesa_integration/static/src/**/*.js',
        ],
    },

    'license': "OPL-1",

    'installable': True,
    'application': True,
}

