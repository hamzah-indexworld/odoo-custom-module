from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Estate Property Tags'

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string='Color')

    # A tag can belong to many properties
    property_ids = fields.Many2many('estate.property', string="Properties")
