# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import networkx as nx


class ResRelation(models.Model):
    _name  = 'res.relation'
    
     
     
    name                   = fields.Char('Nom',compute="compute_name")
    relation_line_ids      = fields.One2many(string='lignes',comodel_name='relation.line.line',inverse_name='relation_id')
    station_line_ids       = fields.One2many(string="Gares",comodel_name="relation.station.line",inverse_name="relation_id")
    start_station_id       = fields.Many2one('res.station', string='Gare de départ', required=True,) 
    end_station_id         = fields.Many2one('res.station', string="Gare d'arrivée", required=True,) 
    amount_distance        = fields.Float("Parcours(KM)",digits=(16, 3))   
    
    def compute_name(self):
        for rec in self:
            rec.name=""
            if rec.start_station_id and rec.end_station_id:
                rec.name = rec.start_station_id.name+" ➜ "+ rec.end_station_id.name

    @api.onchange('relation_line_ids')
    def get_domainfiltre_stations(self):
        station_ids =[]
        for line in self.relation_line_ids:
            for stations in line.line_id.station_line_ids:
                station_ids.append(stations.station_id.id)
        res = {'domain' : {'start_station_id' : [('id', 'in', tuple(station_ids))],
                           'end_station_id' : [('id', 'in', tuple(station_ids))]
                           }}

        return res

    
    @api.onchange('start_station_id','end_station_id')
    def get_stations_list_distance(self):
        self.station_line_ids = None
        self.amount_distance = 0
        if self.start_station_id and self.end_station_id:
            G = nx.Graph()
            for line in self.relation_line_ids:
                for i in range(0, len(line.line_id.station_line_ids)):
                    ln = line.line_id.station_line_ids
                    # if not(G.has_node(ln[i].station_id.id)) :   
                    _logger.warning('\n ok ok ln[i].station_id.name=>%s**%s',ln[i].station_id.name,G.has_node(ln[i].station_id.id))

                    G.add_node(ln[i].station_id.id, pk=ln[i].distance,line_id=ln.line_id.id)

                    if i< len(ln)-1:
                        G.add_edge(ln[i].station_id.id,ln[i+1].station_id.id, distance = ln[i+1].distance - ln[i].distance )
            try :
                path = nx.shortest_path(G,self.start_station_id.id , self.end_station_id.id,weight='distance')
                pathd = nx.shortest_path_length(G,self.start_station_id.id , self.end_station_id.id,weight='distance')
                self.amount_distance =  pathd   
            except:
                path = ()    
               
            if len(path)>0:    
                self.station_line_ids = [(0,0,{'station_id':station_id, 
                                                'line_id'  : G.nodes[station_id].get('line_id'),
                                                'pk'       : G.nodes[station_id].get('pk'),
                                                }) for station_id in path]


class RelationBranchLine(models.Model):

    _name = 'relation.line.line'
    _order = 'sequence'
    _rec_name="line_id"
             
    line_id               = fields.Many2one(comodel_name='res.line',string='Ligne',required=True,ondelete='cascade')
    distance              = fields.Float(string="Distance (KM)", digits=(16, 3) ,related="line_id.amount_distance" )
    relation_id           = fields.Many2one(comodel_name='res.relation',string='Relation',ondelete='cascade')
    sequence              = fields.Integer('Sequence')
  

class RelationStationLine(models.Model):

    _name = 'relation.station.line'

             
    name                  = fields.Char(string='Libellé')
    station_id            = fields.Many2one('res.station', string='Gare', required=True,) 
    pk                    = fields.Float(string="PK" ,digits=(16, 3))
    relation_id           = fields.Many2one(comodel_name='res.relation',string='Relation',ondelete='cascade')
    line_id               = fields.Many2one(comodel_name='res.line',string='Ligne',required=True,ondelete='cascade')
