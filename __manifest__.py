# -*- coding: utf-8 -*-
{
    'name': "odoov14_material",
    'summary': """
        Module for registering and managing materials""",

    'description': """
        This module allows users to register, view, update, and delete materials.
        It includes features for material code, name, type, buy price, and related supplier.
    """,
    'sequence': 10,
    'author': "muhamadalfarisy98@gmail.com",
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts'
                ,
                'purchase'
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/material_views.xml',

        # menu views
        'views/menu_views.xml',

        # data dummy
        'data/supplier_data.xml',      
        'data/material_demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'test': [                   
        'tests/test_material.py', 
    ],
}
