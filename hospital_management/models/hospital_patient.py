from odoo import models, fields, api



class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(required=True, tracking=True)
    age = fields.Integer(required=True, tracking=True)
    blood_group = fields.Char(string='Blood group' ,required=True, tracking=True)



    # relation
    selected_doctor_id = fields.Many2one('hospital.staff', domain="[('role','=','doctor')]")
    slot_ids = fields.One2many('hospital.slot', 'patient_id')
    # fetch only those doctor slots which patient selected.
    available_slot_ids = fields.Many2many('hospital.slot', compute='_compute_available_slots')



    @api.depends('selected_doctor_id')
    def _compute_available_slots(self):
        for record in self:
            if record.selected_doctor_id:
                avail_slots = self.env['hospital.slot'].search([
                        ('doctor_id', '=', record.selected_doctor_id.id),
                        ('status', '=', 'available'),
                    ])
                record.available_slot_ids = avail_slots
            else:
                record.available_slot_ids = self.env['hospital.slot']

