
# -*- coding: utf-8 -*-
from odoo import models, fields, api



class RailroadCrossing(models.Model):

    _name        = 'railroad.crossing'
    _description = 'Passage à niveau'
   
    name               = fields.Char('Numéro de passage à niveau')
    departnet_id       = fields.Many2one('hr.department','Région') 
    res_line_id        = fields.Many2one('res.line','ligne')    
    pk                 = fields.Float('PK',digits=(16, 3)) 
    type               = fields.Char('Type')
    observation        = fields.Text('Observation') 
