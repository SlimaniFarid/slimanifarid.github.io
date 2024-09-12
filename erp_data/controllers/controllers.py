# -*- coding: utf-8 -*-
# from odoo import http


# class ErpData(http.Controller):
#     @http.route('/erp_data/erp_data', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/erp_data/erp_data/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('erp_data.listing', {
#             'root': '/erp_data/erp_data',
#             'objects': http.request.env['erp_data.erp_data'].search([]),
#         })

#     @http.route('/erp_data/erp_data/objects/<model("erp_data.erp_data"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('erp_data.object', {
#             'object': obj
#         })
