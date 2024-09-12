# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class Trainlines(models.Model):

    _name  = 'train.lines'

  
    train_id    = fields.Many2one('res.train',string='Train',)
    line_id     = fields.Many2one('res.line',string='Lignes') 
    start_pk    = fields.Integer('Du PK')
    end_pk      = fields.Integer('Au PK')
    
 
