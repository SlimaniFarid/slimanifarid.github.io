
# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'  
   



    is_spare_part           = fields.Boolean('Est une pièce de rechange') 
    is_strategic_product    = fields.Boolean('Est un produit stratégique') 
    is_freight_product      = fields.Boolean('Est un produit fret')
    generic_code            =  fields.Char('Code générique')   
    tarpaulin_indece        =  fields.Char('indece de bâchage')   

 
    def name_get(self):
            result = []
            for product in self:
                if not(product.is_freight_product):
                    name =  str(product.name)
                elif product.is_freight_product:
                    name =  str(product.name) + (' ['+str(product.generic_code)+'] ' if product.generic_code else '')
                result.append((product.id, name))
            _logger.warning('\n ok ok result=>%s',result)
            return result
      

