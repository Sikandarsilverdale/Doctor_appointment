# -*- coding: utf-8 -*-

from odoo import models


class Module(models.Model):
    _inherit = "ir.module.module"
    """This module help you to select multiple modules and all selected modules 
        can uninstall on a single click.
        Below is the function which is called on server action.
        """
    def module_multiple_uninstall(self):
        # we select ids of the selected modules using active_ids and then perform button_immediate_uninstall()
        modules_uninstall = self.browse(self.env.context.get('active_ids')).button_immediate_uninstall()

