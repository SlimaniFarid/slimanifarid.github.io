# -*- coding: utf-8 -*-
{
    'name': "Données de base",

    'summary': """
       base data""",

    'description': """
       
    """,

    'author': "BENAMROUCHE Djazia & SLIMANI Farid",
    'website': "https://www.sntf.dz",

 
    'category': 'Data',
    'version': '1.0.0',

    'depends': ['base','web','mail','hr','product','sntf_hr'],

    'data': [

        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'data/res_country_state.xml',
        
        'views/rail_network.xml',
        'views/res_station.xml',
        # 'views/res_branch.xml',
        'views/res_relation.xml',
        'views/res_line.xml',
        'views/railroad_crossing.xml',

        'views/res_wcar.xml',
        'views/res_wcar_series.xml',

        'views/spare_parts.xml',
        'views/strategic_products.xml',
        'views/product_freight.xml',
        'views/res_train.xml',
        'views/train_type.xml',
        'views/engine_material.xml',
        'views/res_car.xml',
        'wizard/network_graph.xml',


        'menu/menu.xml',
      
    ],
    'assets': {
        'web.assets_backend': [
            'erp_data/static/src/components/line_graph.js',
            'erp_data/static/src/components/line_graph.xml',
        ],
    }
   
}
