
# -*- coding: utf-8 -*-
from odoo import models, fields, api



class ResLocomotive(models.Model):

    _name        = 'res.locomotive'
    _description = 'Res Locomotive'
   
    name               = fields.Char('Numéro de la locomotive')
    departnet_id       = fields.Many2one('hr.department','Dépot') 
    serie              = fields.Char('Série')
    way                = fields.Selection([('vn', 'VN'),('ve', 'VE')], string='Voie')
    state              = fields.Char('État')
    
