
# -*- coding: utf-8 -*-
from odoo import models, fields, api
import json   
import logging
_logger = logging.getLogger(__name__)
from decimal import Decimal

class ResLine(models.Model):

    _name = 'res.line'


    name                = fields.Char('Nom',compute="get_name",store=True)
    station_line_ids    = fields.One2many('station.line', 'line_id', string='Gares')
    amount_distance     = fields.Float("Parcours(KM)",compute="compute_amount_distance", store=False,digits=(16, 3))    
    rail_network_id     = fields.Many2one('rail.network',string="Réseau ferroviaire")

    @api.depends("station_line_ids","station_line_ids.distance")
    def compute_amount_distance(self):
        for rec in self:
            rec.amount_distance = max([line.distance for line in rec.station_line_ids ]) if len(rec.station_line_ids)>0 else 0
              

    @api.depends("station_line_ids","station_line_ids.distance")
    def get_name(self):
        for rec in self:
            rec.name=""
            if len(rec.station_line_ids)>=2:
                if rec.station_line_ids[0].station_id.name and rec.station_line_ids[-1].station_id.name:
                        rec.name = rec.station_line_ids[0].station_id.name+" ➜ "+rec.station_line_ids[-1].station_id.name
          
    # graph_data          = fields.Text('Branch line data',compute="graph_data") 

    # @api.depends('station_line_ids','station_line_ids.distance')
    # def graph_data(self):
    #     for rec in self:
    #         elements = {"nodes":[],
    #                     "edges":[]}
    #         for branch_line in rec.branch_line_ids:
    #             for branch in branch_line.branch_id:
    #                 for station_line in branch.station_line_ids:
    #                     elements['nodes'].append({ "data": { "id"           : station_line.station_id.id,
    #                                                         "name"          : station_line.station_id.name,
    #                                                         "station_line"  : station_line.id,
    #                                                         "pk"            : station_line.distance,
    #                                                         "last": 1 if station_line.station_id.id == branch.station_line_ids[-1].station_id.id else 0,
    #                                                            } },)
            
    #         i = 0
    #         while i < len(elements['nodes'])-1:
    #             if elements['nodes'][i]['data']['last']==1:
    #                 i+=1
    #             d = elements['nodes'][i]['data']  
    #             d_add_1 = elements['nodes'][i+1]['data']
    #             elements['edges'].append({ 'data': {'id': d['station_line'], 
    #                                               'source': d['id'], 
    #                                               'target': d_add_1['id'], 
    #                                               'distance':round(d_add_1['pk'] - d['pk'], 2)
    #                                               }
    #                                      })
                
    #             i+=1

    #         rec.graph_data = json.dumps(elements)
            




class StationLine(models.Model):

    _name = 'station.line'
    _order = 'distance' 
    rec_name="station_id"
             
    station_id         = fields.Many2one('res.station', string='Gare', required=True,) 
    station_type       = fields.Selection([('travelers','Voyageurs '),('freight','Marchandises'),
                                           ('mixed ','Mixtes'),('stops', 'Haltes'),('workshop', 'Atelier')],
                                            related='station_id.station_type', string='Type de la gare')   

    distance            = fields.Float(string="PK" ,digits=(16, 3))
    line_id             = fields.Many2one(comodel_name='res.line',string='Ligne',required=False)
    sequence            = fields.Integer('Sequence')
    cantonnement_mode   = fields.Selection([('BAL','Block Automatique Lumineux'),
                                            ('BMVU','Block Manuel de Voie Unique'),
                                            ('ct','Cantonnement Téléphonique'),
                                            ('RC','Régulation Complète'),
                                            ('BP','Baton Pilote'),
                                            ('PLO','Poste Local des Operations'),
                                            ('BSE','Block Système Enclenché'),
                                            ('PCC','Poste à Commande Centralisée'),

                                            ],"Mode de cantonnement")
	


    #to ignore selected station and get the name of line
    @api.onchange('station_id')
    def _onchange_station_id(self):
        station_selected_ids=[]
        for line in self.line_id.station_line_ids:
            if line.station_id.id and line.station_id.id not in station_selected_ids:
                station_selected_ids.append(line.station_id.id)                        
     
        res = {'domain' : {'station_id' : [('id', 'not in', tuple(station_selected_ids))]}
                }
        return res

