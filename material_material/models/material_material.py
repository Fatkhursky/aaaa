# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class MaterialMaterial(models.Model):
    _name = 'material.material'
    _description = 'material material'

    material_code = fields.Char(string='Material Code', copy=False)
    material_name = fields.Char(string='Material Name', index=False)
    material_type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton')])
    material_buy_price = fields.Integer(
        string='Buy Price')
    suplier_partner_id = fields.Many2one(
        'res.partner', string='Suplier')
    
    _sql_constraints = [
        ('unique_material_code', 'unique(material_code)', 'Material code must be unique!')
    ]

    total = fields.Float(compute="_compute_total", inverse="_inverse_total")
    amount = fields.Float()
    
    @api.depends("amount")
    def _compute_total(self):
        for record in self:
            record.total = 2.0 * record.amount
    def _inverse_total(self):
        for record in self:
            record.amount = record.total / 2.0

    # @api.constrains('code')
    # def _check_code_unique(self):
    #     # if not self.code:
    #     #      raise UserError(f'''Partner code is required''')
    #     partner = self.search(
    #         [('code', '=', self.code), ('id', '!=', self.id)], limit=1)
    #     if partner:
    #         raise ValidationError(
    #             f'''Partner code {self.code} already exists for Partner:{partner.name}, Address:{partner.street}''')

    @api.constrains('material_buy_price')
    def action_material(self):
        for r in self:
            if r.material_buy_price < 100:
                raise ValidationError(
                    'Buy price cannot be less than 100')
