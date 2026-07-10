from odoo import models, fields



class HospitalStaff(models.Model):
    _name = 'hospital.staff'
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    specialization = fields.Char( tracking=True)
    phone = fields.Char( tracking=True)

    role = fields.Selection([
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse')
    ], required=True)

    # relation
    slot_ids = fields.One2many('hospital.slot', 'doctor_id')
    # patient_ids = fields.Many2many('hospital.patient')

    # message_ids = fields.One2many(
    #     'mail.message',
    #     'res_id',
    #     string='Messages'
    # )
    #
    # activity_ids = fields.One2many(
    #     'mail.activity',
    #     'res_id',
    #     string='Activities'
    # )


#
# Odoo automatically adds:
#
# message_ids
# message_follower_ids
# activity_ids
# message_main_attachment_id
# etc.
#
# You do not declare them yourself.



#
# @api.model_create_multi
# def create(self, vals_list):
#     records = super().create(vals_list)
#
#     for record in records:
#         record.message_post(
#             body="Doctor record created."
#         )
#
#     return records