#-*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class Service_type(models.Model):
    _name = 'data.service_type'


    name        = fields.Char('Préstation', required=True)