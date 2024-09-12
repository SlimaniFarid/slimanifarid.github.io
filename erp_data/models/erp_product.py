#-*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class Erp_product(models.Model):
    _name = 'data.erp_product'


    name            = fields.Char('Nom de l\'article', required=True)
    default_code    = fields.Char('Symbole', required=True)
    standard_price  = fields.Float('Cout',)
    