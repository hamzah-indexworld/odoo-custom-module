{
    'name': 'Estate Module',
    'version': '1.0',
    'depends': ['base', 'website'],
    'data': [
        'security/security.xml',          # 1. ALWAYS FIRST (Creates Categories and Groups)
        'security/ir.model.access.csv',   # 2. SECOND (Assigns permissions to those Groups)
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_users_view.xml',
        'views/estate_actions.xml',
        'views/estate_menus.xml',

        # frontend templates
        'views/frontend_templates.xml',
        'views/portal_property_template.xml',
        
        # reports
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',

    ],
    'demo': [
        'demo/estate_property.csv',
    ],
    'installable': True,
    'application': True,
}