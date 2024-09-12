# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class NetworkGraph(models.TransientModel):
    _name = 'network.graph'
    _description = 'Network graph'



    graph_data    = fields.Text('Data') 