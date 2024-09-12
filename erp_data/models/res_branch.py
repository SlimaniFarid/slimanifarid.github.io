
# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from decimal import Decimal

class ResBranch(models.Model):

    _name = 'res.branch'
    _inherit = 'mail.thread'

    name               = fields.Char('Nom',compute="get_name")
    code               = fields.Char('Code')
    station_line_ids   = fields.One2many(string="Gares",comodel_name="branch.station.line",inverse_name="branch_id",)
    amount_distance    = fields.Float("Parcours(KM)",compute="compute_amount_distance", store=False,digits=(16, 3))    



    @api.depends("station_line_ids","station_line_ids.distance")
    def get_name(self):

        for rec in self:
         
            rec.name=""
            if len(rec.station_line_ids)>=2:
                if rec.station_line_ids[0].station_id.name and rec.station_line_ids[-1].station_id.name:
                        rec.name = rec.station_line_ids[0].station_id.name+" ➜ "+rec.station_line_ids[-1].station_id.name
          

    @api.depends("station_line_ids","station_line_ids.distance")
    def compute_amount_distance(self):
        for rec in self:
            rec.amount_distance = max([line.distance for line in rec.station_line_ids ]) if len(rec.station_line_ids)>0 else 0
              


     
class BranchStationLine(models.Model):

    _name = 'branch.station.line'
    _order = 'distance' 
    rec_name="station_id"
             
    station_id         = fields.Many2one('res.station', string='Gare', required=True,) 
    station_type       = fields.Selection([('travelers','Voyageurs '),('freight','Marchandises'),
                                           ('mixed ','Mixtes'),('stops', 'Haltes'),('workshop', 'Atelier')],
                                            related='station_id.station_type', string='Type de la gare')   

    distance           = fields.Float(string="PK" ,digits=(16, 3))
    branch_id          = fields.Many2one(comodel_name='res.branch',string='Branche',required=False)
    sequence           = fields.Integer('Sequence')

    
 
            
    # to ignore selected station and get the name of line
    @api.onchange('station_id')
    def _onchange_station_id(self):
        station_selected_ids=[]
        for line in self.branch_id.station_line_ids:
            if line.station_id.id and line.station_id.id not in station_selected_ids:
                station_selected_ids.append(line.station_id.id)                        
     
        res = {'domain' : {'station_id' : [('id', 'not in', tuple(station_selected_ids))]}
                }
        return res
        

 