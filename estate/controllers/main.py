from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):

    # This defines the website URL path: http://localhost:8069/properties
    @http.route('/properties', type='http', auth='public', website=True)
    def list_properties(self, **kwargs):
        # 1. Fetch the data from your backend model
        properties = http.request.env['estate.property'].search([])

        # 2. Pass the data to the frontend HTML template
        return http.request.render('estate.property_list_template', {
            'properties': properties
        })



    @http.route('/estate/properties', type='json', auth='public', methods=['GET'])
    def get_available_properties(self):
        properties = request.env['estate.property'].sudo().search([
            ('state', 'in', ['new', 'offer_received'])
        ])

        property_list = []
        for prop in properties:
            property_list.append({
                'id': prop.id,
                'name': prop.name,
                'expected_price': prop.expected_price,
                'bedrooms': prop.bedrooms,
                'living_area': prop.living_area,
            })

        return {
            'status': 200,
            'data': property_list
        }



    @http.route('/estate/property/create', type='http', auth='user', methods=['POST'], csrf=True)
    def create_property_inquiry(self, **post):
        if not post.get('name') or not post.get('expected_price'):
            return "Missing required fields: name or expected_price"

        # Create the record in the database
        new_property = request.env['estate.property'].create({
            'name': post.get('name'),
            'expected_price': float(post.get('expected_price')),
            'bedrooms': int(post.get('bedrooms', 0)),
            'description': post.get('description', ''),
        })

        # Redirect the user to a thank you page or back to the property list
        return request.redirect('/estate/properties/success?id=%s' % new_property.id)




    @http.route(['/my/properties'], type='http', auth='portal', website=True)
    def portal_my_properties(self, **kw):
        # We only search for properties where the current portal user is linked
        # e.g., matching their partner_id
        partner = request.env.user.partner_id
        properties = request.env['estate.property'].sudo().search([
            ('buyer_id', '=', partner.id)
        ])

        # Pass the records to a frontend XML template
        return request.render('estate.portal_my_properties_template', {
            'properties': properties,
        })