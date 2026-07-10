from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU


class HospitalSlot(models.Model):
    _name = 'hospital.slot'

    slot_date = fields.Date(required=True)
    start_time = fields.Float(required=True)
    end_time = fields.Float(required=True)
    # slot_duration = fields.Integer(string='Duration', default=20, required=True)

    status = fields.Selection([
        ('booked', 'Booked'),
        ('available', 'Available'),
    ] , default='available', required=True, compute='_compute_slot_status', store=True)

    select_appointment = fields.Boolean(string="Select appointment", default=False)

    # related field
    specialization = fields.Char('specialization', related='doctor_id.specialization', readonly=True)

    # relation
    # doctor_id = fields.Many2one('hospital.doctor')
    patient_id = fields.Many2one('hospital.patient')


    # new relation 
    doctor_id = fields.Many2one('hospital.staff', domain=[('role', '=', 'doctor')])


    @api.depends('patient_id')
    def _compute_slot_status(self):
        for record in self:
            if record.patient_id:
                record.status = 'booked'
            else:
                record.status = 'available'


    # @api.constrains('doctor_id' ,'start_time', 'end_time')
    def _check_slot_overlap(self):
        for record in self:
            if not record.doctor_id or not record.start_time or not record.end_time:
                continue

            overlapping_slots = self.env['hospital.slot'].search([
                ('doctor_id', '=', record.doctor_id.id),
                ('start_time', '>=', record.start_time),
                ('end_time', '<=', record.end_time),
                ('id', '!=', record.id),
            ])

            if overlapping_slots:
                raise ValidationError(
                    f"The time slot from {record.start_time} to {record.end_time} "
                    f"overlaps with an existing slot for this doctor."
                )


    @api.onchange('select_appointment')
    def _onchange_select_appointment(self):
        for record in self:
            if record.select_appointment:
                patient_id_from_context = self.env.context.get('current_patient_id')

                if patient_id_from_context:
                    record.patient_id = patient_id_from_context
            else:
                record.patient_id = False


    def action_book_slot(self):
        for record in self:
            current_patient_id = self.env.context.get('current_patient_id')
            if current_patient_id:
                # sudo() bypasses the patient's write restriction just for this action!
                record.sudo().write({
                    'patient_id': current_patient_id,
                })


    # slots by weekdays
    def action_generate_slots(self):
        self.ensure_one()

        if self.start_time >= self.end_time:
            raise ValidationError("End time must be greater than start time.")

        if self.slot_duration <= 0:
            raise ValidationError("Slot duration must be greater than zero.")

        current_start = self.start_time

        while current_start < self.end_time:

            current_end = current_start + timedelta(minutes=self.slot_duration)

            if current_end > self.end_time:
                break

            self.env['hospital.slot'].create({
                'doctor_id': self.doctor_id.id,
                'start_time': current_start,
                'end_time': current_end,
                'slot_duration': self.slot_duration,
                'status': 'available',
            })

            current_start = current_end

        return {
            'type': 'ir.actions.act_window_close',
        }