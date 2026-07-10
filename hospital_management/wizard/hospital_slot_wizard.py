
from odoo import models, fields
from odoo.exceptions import  ValidationError
from datetime import date, datetime, time, timedelta
from calendar import monthrange



class HospitalSlotWizard(models.TransientModel):
    _name = 'hospital.slot.wizard'

    doctor_id = fields.Many2one('hospital.staff', required=True, domain=[('role', '=', 'doctor')])

    weekday_ids = fields.Many2many(
        'hospital.weekday',
        string='Days'
    )

    start_time = fields.Float(required=True)

    end_time = fields.Float(required=True)

    slot_duration = fields.Integer(default=20)



    # wizard action
    def action_generate_slots(self):
        self.ensure_one()

        if not self.weekday_ids:
            raise ValidationError("Please select at least one weekday.")

        if self.start_time >= self.end_time:
            raise ValidationError("End time must be greater than start time.")

        if self.slot_duration <= 0:
            raise ValidationError("Slot duration must be greater than zero.")


        today = fields.Date.context_today(self)

        last_day = monthrange(today.year, today.month)[1]
        end_of_month = today.replace(day=last_day)

        selected_days = [day.code for day in self.weekday_ids]

        current_date = today

        while current_date <= end_of_month:

            if current_date.weekday() in selected_days:

                current_start = self.start_time

                while current_start < self.end_time:

                    current_end = current_start + (self.slot_duration / 60.0)

                    if current_end > self.end_time:
                        break

                    # Prevent duplicate slots
                    existing = self.env['hospital.slot'].search([
                        ('doctor_id', '=', self.doctor_id.id),
                        ('slot_date', '=', current_date),
                        ('start_time', '=', current_start),
                        ('end_time', '=', current_end),
                    ], limit=1)

                    if not existing:
                        self.env['hospital.slot'].create({
                            'doctor_id': self.doctor_id.id,
                            'slot_date': current_date,
                            'start_time': current_start,
                            'end_time': current_end,
                            # 'slot_duration': self.slot_duration,
                        })

                    current_start = current_end

            current_date += timedelta(days=1)

        return {
            'type': 'ir.actions.act_window_close',
        }