
# -*- coding: utf-8 -*-
from odoo import models, fields, api



class EngineMaterial(models.Model):

    _name        = 'engine.material'
    _description = 'Engine Material'
   
    name               = fields.Char('Numéro')
    departnet_id       = fields.Many2one('hr.department',"Établissement d'affectation") 
    serie              = fields.Char('Série')
    way                = fields.Selection([('vn', 'VN'),('ve', 'VE')], string='Voie')
    state              = fields.Char('État')
    material_type      = fields.Selection([('locomotive', 'Locomotive'),('handcar', 'Draisine')], string='Type de matériel')
   #handcar fields
    handcar_type       = fields.Char(string='Type de la Draisine') 
    brand              = fields.Char(string="Marque")
    acquisition_date   = fields.Char("Date d'acquisition")  
    observation        = fields.Text("")