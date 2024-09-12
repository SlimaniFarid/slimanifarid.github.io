#-*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class Maintenance_type(models.Model):
    _name = 'data.maintenance_type'


    name        = fields.Char('Type', required=True)
   