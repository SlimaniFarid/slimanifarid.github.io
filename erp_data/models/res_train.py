# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class ResTrain(models.Model):

    _name  = 'res.train'

    name                = fields.Char(string="Numéro de train", required=True)
    train_type_id       = fields.Many2one('train.type',string='Type de train')
    start_station_id    = fields.Many2one('res.station',string='Gare de départ',related="relation_id.start_station_id")
    end_station_id      = fields.Many2one('res.station',string="Gare d'arrivée",related="relation_id.end_station_id")
    departure_time      = fields.Float(string="Heure de départ")
    arrival_time        = fields.Float(string="Heure d'arriveé")
    start_pk            = fields.Float('PK Début',digits=(16, 3), compute="get_start_pk") 
    end_pk              = fields.Float('PK Fin',digits=(16, 3),compute="get_end_pk") 
    state               = fields.Selection(string="Etat", selection=[('active', 'En circulation'), ('disable', 'Supprimé de la circulation'), ], default="active",)  
    relation_id         = fields.Many2one('res.relation', string='Relation')  
    region_ids          = fields.Many2many('hr.department', string='Régions',domain=[('is_drf','=',True)],compute="get_regions")
    line_ids            = fields.Many2many('res.line', string='Lignes', compute="get_lines") 
    amount_distance     = fields.Float("Parcours(KM)",digits=(16, 3),related="relation_id.amount_distance")  
    travel_time         = fields.Float(string="Temps de parcours", compute="get_travel_time")   



    @api.depends('relation_id')
    def get_regions(self):
        
        for rec in self:
            rec.region_ids = None
            region_ids = [] 
            for line in rec.relation_id.station_line_ids:
                if line.station_id.region_id.id and line.station_id.region_id.id not in region_ids :
                    region_ids.append(line.station_id.region_id.id)
               
            rec.region_ids = region_ids 
    
    
    @api.depends('relation_id')
    def get_lines(self):
        for rec in self:
            rec.line_ids = None
            line_ids =[] 
            for line in rec.relation_id.relation_line_ids:
                if line.line_id.id and line.line_id.id not in line_ids :
                    line_ids.append(line.line_id.id)
            rec.line_ids = line_ids 
    
    @api.depends('relation_id')
    def get_start_pk(self):
        for rec in self:
            rec.start_pk = 0
            for line in rec.relation_id.station_line_ids:
                if line.station_id.id == rec.relation_id.start_station_id.id :
                    rec.start_pk = line.pk
   
    @api.depends('relation_id')
    def get_end_pk(self):
        for rec in self:
            rec.end_pk = 0
            for line in rec.relation_id.station_line_ids:
                if line.station_id.id == rec.relation_id.end_station_id.id :
                    rec.end_pk = line.pk
                    
    @api.depends('arrival_time','departure_time')     
    def get_travel_time(self):
        for rec in self:
            travel_time = rec.arrival_time - rec.departure_time
            if travel_time < 0:
                rec.travel_time = 24 + travel_time
            else :
                 rec.travel_time = travel_time    
            _logger.warning('\n ko ok rec.arrival_time=>%s',rec.arrival_time)
            _logger.warning('\n ko ok travel_time=>%s',travel_time)