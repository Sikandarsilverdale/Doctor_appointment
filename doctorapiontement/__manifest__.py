# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Doctor Appointment Management',
    'version': '1.1',
    'summary': 'Doctor appointment management system',
    'sequence': -100,
    'author': 'odoo',
    'company': 'odoo company',
    'description': """odoo module for Doctor appointment management

    """,
    'category': 'productivity',
    'website': 'https://www.odoo.com',
    'depends': ['base','website_calendar','report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient.xml',
        'views/template.xml',
        'report/patient_detail_template.xml',
        'report/report.xml'

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

    'license': 'LGPL-3',
}
