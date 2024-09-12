
# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import RedirectWarning, UserError, ValidationError
import random
data = [
    {"Type": "PHOSPHATIERS", "Catégorie": "DO", "r_echange": 21, "PW": 92, "Numéro de série": 563, "start": 1, "end": 404},
    {"Type": "PHOSPHATIERS", "Catégorie": "DO", "r_echange": 31, "PW": 92, "Numéro de série": 564, "start": 1, "end": 100},
    {"Type": "PHOSPHATIERS", "Catégorie": "DO", "r_echange": 31, "PW": 92, "Numéro de série": 583, "start": 7001, "end": 7233},
    {"Type": "PHOSPHATIERS", "Catégorie": "DO-(P)", "r_echange": 33, "PW": 92, "Numéro de série": 540, "start": 1, "end": 75},
    {"Type": "WAGON DE SERVICE", "Catégorie": "FOURGON", "r_echange": 80, "PW": 92, "Numéro de série": 972, "start": 101, "end": 661},
    {"Type": "WAGON DE SERVICE", "Catégorie": "FOURGON", "r_echange": 80, "PW": 92, "Numéro de série": 973, "start": 1, "end": 195},
    # {"Type": "WAGON DE SERVICE", "Catégorie": "FOURGON", "r_echange": 80, "PW": 92, "Numéro de série": 974, "start": None, "end": None},
    {"Type": "WAGON DE SERVICE", "Catégorie": "FOURGON", "r_echange": 82, "PW": 92, "Numéro de série": 975, "start": 84, "end": 108},
    {"Type": "WAGON DE SERVICE", "Catégorie": "FOURGON", "r_echange": 82, "PW": 92, "Numéro de série": 976, "start": 1, "end": 55},
    {"Type": "BALLASTIERS", "Catégorie": "SV-Ball", "r_echange": 80, "PW": 92, "Numéro de série": 971, "start": 1, "end": 610},
    {"Type": "BALLASTIERS", "Catégorie": "SV-Ball", "r_echange": 82, "PW": 92, "Numéro de série": 981, "start": 1, "end": 90},
    {"Type": "WAGON DE SERVICE", "Catégorie": "FOURGON", "r_echange": 40, "PW": 92, "Numéro de série": 949, "start": 201, "end": 275},
    {"Type": "COUVERTS", "Catégorie": "IK", "r_echange": 31, "PW": 92, "Numéro de série": 275, "start": 1, "end": 200},
    {"Type": "COUVERTS", "Catégorie": "IK", "r_echange": 31, "PW": 92, "Numéro de série": 285, "start": 1, "end": 200},
    {"Type": "COUVERTS", "Catégorie": "KK", "r_echange": 21, "PW": 92, "Numéro de série": 120, "start": 192, "end": 1147},
    {"Type": "COUVERTS", "Catégorie": "WK", "r_echange": 32, "PW": 92, "Numéro de série": 190, "start": 1, "end": 700},
    {"Type": "COUVERTS", "Catégorie": "GABS", "r_echange": 31, "PW": 92, "Numéro de série": 181, "start": 1, "end": 1000},
    {"Type": "PLATS", "Catégorie": "SPU", "r_echange": 21, "PW": 92, "Numéro de série": 990, "start": 1003, "end": 1007},
    {"Type": "PLATS", "Catégorie": "SPU", "r_echange": 21, "PW": 92, "Numéro de série": 990, "start": 3001, "end": 3020},
    {"Type": "PLATS", "Catégorie": "SPU", "r_echange": 21, "PW": 92, "Numéro de série": 990, "start": 5004, "end": 5010},
    {"Type": "PLATS", "Catégorie": "SSY", "r_echange": 31, "PW": 92, "Numéro de série": 992, "start": 4001, "end": 4020},
    {"Type": "PLATS", "Catégorie": "RORY", "r_echange": 31, "PW": 92, "Numéro de série": 380, "start": 1, "end": 92},
    {"Type": "PLATS", "Catégorie": "RORY", "r_echange": 31, "PW": 92, "Numéro de série": 390, "start": 1, "end": 439},
    {"Type": "PLATS", "Catégorie": "RORY", "r_echange": 31, "PW": 92, "Numéro de série": 393, "start": 6001, "end": 6750},
    {"Type": "PLATS", "Catégorie": "NN", "r_echange": 21, "PW": 92, "Numéro de série": 336, "start": 1, "end": 250},
    {"Type": "PLATS", "Catégorie": "WNY", "r_echange": 32, "PW": 92, "Numéro de série": 394, "start": 8001, "end": 8200},
    {"Type": "PLATS", "Catégorie": "WNY", "r_echange": 32, "PW": 92, "Numéro de série": 395, "start": 5001, "end": 5100},
    {"Type": "PLATS", "Catégorie": "WNY-P/C", "r_echange": 32, "PW": 92, "Numéro de série": 395, "start": 1001, "end": 1500},
    {"Type": "PLATS", "Catégorie": "WSP", "r_echange": 32, "PW": 92, "Numéro de série": 461, "start": 9171, "end": 9245},
    {"Type": "PLATS", "Catégorie": "WSP", "r_echange": 32, "PW": 92, "Numéro de série": 471, "start": 9001, "end": 9350},
    {"Type": "PLATS", "Catégorie": "WSP-ANP", "r_echange": 32, "PW": 92, "Numéro de série": 386, "start": 3001, "end": 3100},
    {"Type": "TOMBEREAUX", "Catégorie": "WNT", "r_echange": 32, "PW": 92, "Numéro de série": 592, "start": 7901, "end": 8210},
    {"Type": "TOMBEREAUX", "Catégorie": "TT", "r_echange": 21, "PW": 92, "Numéro de série": 511, "start": 1, "end": 100},
    {"Type": "TOMBEREAUX", "Catégorie": "WT", "r_echange": 32, "PW": 92, "Numéro de série": 592, "start": 7001, "end": 7615},
    {"Type": "TOMBEREAUX", "Catégorie": "WT", "r_echange": 31, "PW": 92, "Numéro de série": 592, "start": 9001, "end": 9300},
    {"Type": "CITERNES", "Catégorie": "SC-ACIDE", "r_echange": 31, "PW": 92, "Numéro de série": 788, "start": 1, "end": 30},
    {"Type": "CITERNES", "Catégorie": "SC", "r_echange": 31, "PW": 92, "Numéro de série": 780, "start": 1, "end": 100},
    {"Type": "CITERNES", "Catégorie": "SC", "r_echange": 31, "PW": 92, "Numéro de série": 785, "start": 1, "end": 460},
    {"Type": "CITERNES", "Catégorie": "WSC", "r_echange": 32, "PW": 92, "Numéro de série": 780, "start": 1001, "end": 1625},
    {"Type": "CITERNES", "Catégorie": "WSC-MELASSE", "r_echange": 32, "PW": 92, "Numéro de série": 734, "start": 5001, "end": 5050},
    {"Type": "CEREALIERS", "Catégorie": "IB", "r_echange": 31, "PW": 92, "Numéro de série": 584, "start": 3001, "end": 3949},
    {"Type": "CEREALIERS", "Catégorie": "IB-(P)", "r_echange": 33, "PW": 92, "Numéro de série": 584, "start": 3971, "end": 3980},
    {"Type": "CEREALIERS", "Catégorie": "WIB", "r_echange": 32, "PW": 92, "Numéro de série": 584, "start": 4001, "end": 4260},
    {"Type": "IPS", "Catégorie": "A.H", "r_echange": 31, "PW": 92, "Numéro de série": 477, "start": 7001, "end": 7190},
    {"Type": "COUVERTS", "Catégorie": "GAS", "r_echange": 31, "PW": 92, "Numéro de série": 191, "start": 1, "end": 150},
    {"Type": "SABLIERS", "Catégorie": "SV-Sab", "r_echange": 31, "PW": 92, "Numéro de série": 694, "start": 1, "end": 60},
    {"Type": "SABLIERS", "Catégorie": "SV-Sab", "r_echange": 32, "PW": 92, "Numéro de série": 694, "start": 2001, "end": 2020},
    {"Type": "IPS", "Catégorie": "A.H", "r_echange": 31, "PW": 92, "Numéro de série": 476, "start": 3001, "end": 3160},
    {"Type": "IPS", "Catégorie": "A.V", "r_echange": 31, "PW": 92, "Numéro de série": 477, "start": 9001, "end": 9100},
    {"Type": "SPECIAUX-DIVERS", "Catégorie": "SUCRIERS", "r_echange": 31, "PW": 92, "Numéro de série": 569, "start": 2001, "end": 2030},
    {"Type": "SPECIAUX-DIVERS", "Catégorie": "SUCRIERS", "PW": 92, "r_echange":0,"Numéro de série": 114, "start": 1, "end": 28},
    {"Type": "SPECIAUX-DIVERS", "Catégorie": "SALINIERS-SV", "r_echange": 31, "PW": 92, "Numéro de série": 566, "start": 7201, "end": 7405},
    {"Type": "SPECIAUX-DIVERS", "Catégorie": "CASTINE", "r_echange": 31, "PW": 92, "Numéro de série": 665, "start": 151, "end": 195},
    {"Type": "SPECIAUX-DIVERS", "Catégorie": "COKE-CHARBON", "PW": 92,"r_echange":0, "Numéro de série": 610, "start": 1, "end": 76},
    {"Type": "SPECIAUX-DIVERS", "Catégorie": "COKE", "PW": 92, "r_echange":0,"Numéro de série": 665, "start": 1, "end": 40},
    {"Type": "SPECIAUX-DIVERS", "Catégorie": "GYPSE", "r_echange": 31, "PW": 92, "Numéro de série": 566, "start": 7001, "end": 7080},
    {"Type": "SPECIAUX-DIVERS", "Catégorie": "GYPSE", "r_echange": 82, "PW": 92, "Numéro de série": 570, "start": 1, "end": 20},
    {"Type": "MINERALIERS", "Catégorie": "OZ", "r_echange": 31, "PW": 92, "Numéro de série": 662, "start": 5251, "end": 5926},
    {"Type": "SPECIAUX-DIVERS", "Catégorie": "CIMENTIERS", "r_echange": 31, "PW": 92, "Numéro de série": 930, "start": 5001, "end": 5177},
    {"Type": "COUVERTS", "Catégorie": "WK", "r_echange": 32, "PW": 92, "Numéro de série": 180, "start": 24, "end": 123},
    {"Type": "PHOSPHATIERS", "Catégorie": "DO", "r_echange": 31, "PW": 92, "Numéro de série": 583, "start": 7300, "end": 7679},
    {"Type": "CITERNES", "Catégorie": "SC (P)", "r_echange": 33, "PW": 92, "Numéro de série": 790, "start": 1, "end": 20}


]


class ResWCar(models.Model):

    _name        = 'res.wcar'
    _description = 'Wagons'
    
   
    name                  = fields.Char('Numéro de wagon')
    series_id             = fields.Many2one(string='Série',comodel_name="res.wcar.series")    
    verification_code     = fields.Char(string='Code de vérification',compute="compute_verification_code")
    latitude              = fields.Float('Latitude',digits=(2,10))
    longitude             = fields.Float('Longitude',digits=(2,10))
    designation_serie     = fields.Char('Désignation série',related="series_id.name") 
    boggie                = fields.Integer('N° Boggie')
    axle                  = fields.Integer('N° Essieu')
    interchangeable_code  = fields.Integer(string='Code interchangeable')
    reseau_sntf           = fields.Integer('Réseau SNTF') 
    partner_id            = fields.Many2one('res.partner',string='Client')
    volume                = fields.Float(string='Volume m³')   
    max_tonnage           = fields.Float(string='Tonnage maximum')  
    state                 = fields.Selection(string='Etat', selection=[('loaded', 'Chargé'),('unloaded','Déchargé')])
    station_id            = fields.Many2one(string="Gare",comodel_name="res.station")    
    state_id              = fields.Many2one('res.country.state',string='wilaya Desservie',)
    region_id             = fields.Many2one('hr.department',string='Région')

    #to create all wagong and series
    def test(self):
        for d in data:
            serie = self.env['res.wcar.series'].create({'name':d['Numéro de série'],'category':d['Catégorie'],'type':d['Type']})
            for i in range(d['start'], d['end']+1):
                self.create({'name': i,'series_id': serie.id,'interchangeable_code':d["r_echange"],'reseau_sntf':d['PW']})
       





    @api.onchange('station_id')
    def _onchange_station_id(self):
        self.latitude = 0
        self.longitude = 0
        self.state_id =  False   
        self.region_id = False
        if self.station_id:
            self.latitude   = self.station_id.latitude
            self.longitude  = self.station_id.longitude
            self.state_id   = self.station_id.state_id
            self.region_id  = self.station_id.region_id

    def get_all_name(self,ids):
        names="<ul>"
        wcar_names  = self.search([('id', 'in', ids)])
        for wcar_name in wcar_names :
            names+= "<li>" + wcar_name.name +"</li>"
        names+"</ul>"    
        return names

    def name_get(self):
        result = []
        for wcar in self:
            name = str(wcar.name)+'-'+str(wcar.verification_code)
            if wcar.partner_id:
                name += ' ('+ wcar.partner_id.name + ')' 

            result.append((wcar.id, name))
        return result
          


    @api.depends('name','series_id')
    def compute_verification_code(self):
        for rec in self:
            verification_code = -1
            if rec.reseau_sntf and rec.interchangeable_code and len(rec.name)>= 4:
                tab1 = [2,1,2,1,2,1,2,1,2,1,2]
                tab2=[int(x) for x in str(rec.interchangeable_code)]
                tab2+=[int(x) for x in str(rec.reseau_sntf)]
                tab2+=[int(x) for x in str(rec.series_id.code)]
                tab2+=[int(x) for x in str(rec.name)]
                i=0
                tab3=[]
                tab4=[]

                while i <len(tab1):
                  
                    tab3+=[tab1[i] * tab2[i]]   
                    i+=1
                for v in tab3:
                  tab4 += [int(x) for x in str(v)]   
                code =  int(str(sum(tab4))[-1]) 
                if code == 0:
                    verification_code = 0
                else:
                    verification_code = 10-code
            if verification_code == -1:
                rec.verification_code = (random.randint(100, 200))
            else :    
                rec.verification_code = verification_code
        
        
    @api.onchange('verification_code')
    def onchange_verification_code(self):
        if len(str(self.verification_code))>2 and self.name and len(self.name)>1 :
            return {
                    'warning': {
                        'title':"Attention !",
                        'message': "Veuillez vérifier le numéro de wagon"
                    }
                }
   ##############################################################################     