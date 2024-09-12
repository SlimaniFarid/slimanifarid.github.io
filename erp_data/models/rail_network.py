# -*- coding: utf-8 -*-
from odoo import models, fields, api
import json   
import logging
_logger = logging.getLogger(__name__)




class RailNetwork(models.Model):
    _name  = 'rail.network'

    name          = fields.Char("Nom")
    company_id    = fields.Many2one("res.company","Opérateur",)
    station_ids   = fields.Char()
    line_ids      = fields.One2many(string="Lignes",comodel_name="res.line",inverse_name="rail_network_id",)
    graph_data    = fields.Text('Data',compute="compute_graph_data") 

    def action_get_graph(self):
        self.ensure_one()
      
        return {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'network.graph',
            'context': {"create": False, 'default_graph_data': self.graph_data},
            'target': 'new',
        }


    @api.depends('line_ids')
    def compute_graph_data(self):
        for rec in self:
            elements = {"nodes":[],
                        "edges":[]}
            staion_ids = []
            arc = []
            for lines in rec.line_ids:
                for i in range(0, len(lines.station_line_ids)):    
                    ln = lines.station_line_ids
                    if ln[i].station_id.id not in staion_ids :
                        node = { "data": { "id" : ln[i].station_id.id,"name" : ln[i].station_id.name,
                                            "station_line"  : ln[i].id,"pk" : ln[i].distance,} }
                        if ln[i].station_id.name=='ATELIERS':
                            _logger.warning('\n ok ok station %s ** pk=>%s',ln[i].station_id.name, ln[i].distance)
                                        
                        elements['nodes'].append(node)
                        staion_ids.append(ln[i].station_id.id)

                    if i< len(ln)-1 :  
                        if (ln[i].station_id.id,ln[i+1].station_id.id) not in arc:
                            edge =  { 'data': {'id': ln[i].id, 
                                                'source': ln[i].station_id.id, 
                                                'target': ln[i+1].station_id.id, 
                                                'distance':round(ln[i+1].distance - ln[i].distance, 2)
                                                    }}
                            arc.append((ln[i].station_id.id,ln[i+1].station_id.id))
                            elements['edges'].append(edge)

            rec.graph_data = json.dumps(elements)