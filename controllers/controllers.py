# -*- coding: utf-8 -*-
# from odoo import http


# class Odoov14Material(http.Controller):
#     @http.route('/odoov14_material/odoov14_material/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoov14_material/odoov14_material/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoov14_material.listing', {
#             'root': '/odoov14_material/odoov14_material',
#             'objects': http.request.env['odoov14_material.odoov14_material'].search([]),
#         })

#     @http.route('/odoov14_material/odoov14_material/objects/<model("odoov14_material.odoov14_material"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoov14_material.object', {
#             'object': obj
#         })
