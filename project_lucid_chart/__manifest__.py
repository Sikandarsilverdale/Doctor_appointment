# -*- coding: utf-8 -*-
{
    "name": "Project Lucid Chart",
    "summary": """This module add a tab on project form and in this tab lucid chart is change on the change of url""",
    "description": """
       This module add a tab on project form and in this tab lucid chart is change on the change of url.
    """,
    "author": "Silverdale",
    "website": "https://wwww.silverdaletech.com",
    "version": "15.0",
    'license': 'OPL-1',
    "images": ["static/description/main_screenshot.png"],
    "depends": ["base", "project"],

    "data": [
        'security/ir.model.access.csv',
        'views/project_view.xml'

    ],

    "application": False,
    "installable": True,
    "auto_install": False,
}