#-*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class Operation_type(models.Model):
    _name = 'data.operation_type'


    name        = fields.Char('Opération', required=True)