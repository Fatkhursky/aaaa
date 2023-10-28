# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class a_material(models.Model):
#     _name = 'a_material.a_material'
#     _description = 'a_material.a_material'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
