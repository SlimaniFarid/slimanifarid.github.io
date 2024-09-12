
# -*- coding: utf-8 -*-
from odoo import models, fields, api



class ResCar(models.Model):

    _name        = 'res.car'
    _description = 'Voitures'
   
    name               = fields.Char('Numéro de la voiture',required=True)
    type_id            = fields.Many2one('res.type.car','Type') 
    series_id          = fields.Many2one('res.series.car','Série') 
    department_id      = fields.Many2one('hr.department',"Établissement d'attache")
    state              = fields.Char('État')    


class ResTypeCar(models.Model):

    _name        = 'res.type.car'
    _description = 'Type des voitures'
   
    name               = fields.Char('Numéro de la voiture',required=True)

    
        
    
class ResSeriesCar(models.Model):

    _name        = 'res.series.car'
    _description = 'série des voitures'
   
    name               = fields.Char('Nom',required=True)

    
