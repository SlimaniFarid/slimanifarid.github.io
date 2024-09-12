# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class erp_data(models.Model):
#     _name = 'erp_data.erp_data'
#     _description = 'erp_data.erp_data'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
