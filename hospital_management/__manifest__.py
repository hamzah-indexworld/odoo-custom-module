{
    'name': 'Hospital Management',
    'version': '1.0',
    'category': 'Hospital Management',
    'description': 'this module is for testing',
    'author': 'hamza farooq',
    'website': 'https://www.farooq.com/',
    'depends': ['base', 'mail'],
    'data': [
        # security
        'security/security.xml',
        'security/ir.model.access.csv',

        # actions
        'views/hospital_actions.xml',

        # views
        'views/hospital_doctor_views.xml',
        'wizard/hospital_slot_wizard_views.xml',
        'views/hospital_patient_views.xml',
        'views/hospital_slot_views.xml',
        'views/hospital_staff_nurse.xml',
        'views/hospital_staff_doctor.xml',
        'views/hospital_menus.xml',

    ],
    'application': True,
    'installable': True,
}