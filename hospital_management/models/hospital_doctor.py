from odoo import models, fields



class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'

    name = fields.Char(required=True)
    specialization = fields.Char(required=True)
    phone = fields.Char()


    # relation
    slot_ids = fields.One2many('hospital.slot', 'doctor_id')
    patient_ids = fields.Many2many('hospital.patient')


