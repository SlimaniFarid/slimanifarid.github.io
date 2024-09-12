# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.modules.module import get_module_resource
import base64

class ResStation(models.Model):

     _name =      'res.station'
     _inherit = ['image.mixin']

     def get_default_rail_network(self):
          company_d = self.env['rail.network'].search([('company_id','=',self.env.user.company_id.id)]).id
          return company_d


     name             =  fields.Char(string="Nom",required=True)
     code             =  fields.Char(string="Code")
     name_arabe       =  fields.Char(string="Nom en arabe")
     station_type     =  fields.Selection([('travelers','Voyageurs '),('freight','Marchandises'),('mixed ','Mixtes'),('stops', 'Haltes'),('workshop', 'Atelier')], string='Type de la gare')   
     
     state_id         =  fields.Many2one('res.country.state',string='Wilaya Desservie',domain=[('country_id','=',62)])
     longitude        =  fields.Float(string='Longitude',digits=(2,10))
     latitude         =  fields.Float(string="latitude",digits=(2,10))
     region_id        =  fields.Many2one('hr.department',string='Région')

     rail_network_id  =  fields.Many2one(string='Réseau ferroviaire', comodel_name='rail.network', default=get_default_rail_network)
