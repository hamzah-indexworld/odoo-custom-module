from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property a custom module for testing'
    _order = 'id desc'

    # sequence = fields.Integer(string="Sequence", default=1)
    color = fields.Integer(string='Color')
    name = fields.Char(string='Name', required=True, help='Name of the property')
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=3, copy=False)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )

    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted') ,('sold', 'Sold'), ('cancelled', 'Cancelled')],
        string="State",
        default='new',
        required=True,
        copy=False
    )


    # date_start = fields.Date(string="Start Date", default=fields.Date.today)
    date_availability = fields.Date(string="Available From", copy=False, default=fields.Date.context_today)

    active = fields.Boolean(default=True)
    total_area = fields.Integer(string="Total Area", compute='_compute_total_area')
    best_offer = fields.Float(string='Best Offer', compute='_compute_best_offer')

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self:self.env.user)
    tag_ids = fields.Many2many('estate.property.tags', string='Tags')
    # offer_ids = fields.One2many('estate.property.offer', string='Offers')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers', ondelete='cascade')


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # def _inverse_total_area(self):


    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                price_list = []
                for offer in record.offer_ids:
                    price_list.append(offer.price)

                record.best_offer = max(price_list)
            else:
                record.best_offer = 0.00


    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False


    def action_sold_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('property is cancelled')
            else:
                record.state = 'sold'
        return True


    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('property is already sold')
            else:
                record.state = 'cancelled'
        return True


    # validation
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'the expected price should be greater than 0'
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price == 0:
                continue

            required_price = record.expected_price * 0.90
            if record.selling_price < required_price:
                raise ValidationError('selling_price must be greater than 90% of expected_price')
        return True