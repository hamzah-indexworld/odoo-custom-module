from odoo import models, fields


class HospitalWeekday(models.Model):
    _name = 'hospital.weekday'
    _description = 'Weekday'

    name = fields.Char(required=True)
    code = fields.Integer(required=True)