# -*- coding: utf-8 -*-
from odoo import models, fields, api



class TrainType(models.Model):
     _name = 'train.type'

     name  =  fields.Char("Type de train")

    