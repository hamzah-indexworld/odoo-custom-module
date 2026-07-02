from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False)
    buyer_id = fields.Many2one("res.partner", string="Buyer", required=True, ondelete='cascade')
    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete='cascade')

    property_type_id = fields.Many2one("estate.property.type",related="property_id.property_type_id",string="Property Type",store=True)


    def action_accept_property_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.buyer_id
        return True


    def action_reject_property_offer(self):
        for record in self:
            record.status = 'refused'
        return True