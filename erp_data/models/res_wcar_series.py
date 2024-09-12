
# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class ResWCarSeries(models.Model):

    _name        = 'res.wcar.series'
    _description = 'Série des Wagons'
    _rec_name    = "name"
   
    name              = fields.Char('N° de la série')
    category          = fields.Char('Catégorie')
    type              = fields.Char('Type')

    start_wcar_number = fields.Char('Du wagon n°', compute='compute_start_and_wcar_number')
    end_wcar_number   = fields.Char('Au wagon n°', compute='compute_start_and_wcar_number')
    wcar_ids          = fields.One2many(string="Wagons", comodel_name="res.wcar", inverse_name='series_id')
  
    @api.depends('wcar_ids')
    def compute_start_and_wcar_number(self):
        for rec in self:
            rec.start_wcar_number = False
            rec.end_wcar_number   = False       
            # car_ids = self.env['res.wcar'].search([('id','in',rec.wcar_ids.ids)],order="name asc")
            if len(rec.wcar_ids)>1:
                rec.start_wcar_number=rec.wcar_ids[0].name 
                rec.end_wcar_number=rec.wcar_ids[-1].name 

    
    