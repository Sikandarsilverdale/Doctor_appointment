# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProjectForm(models.Model):
    _name = 'project.project'
    _inherit = ['project.project', 'mail.activity.mixin']

    luci_chart_url = fields.Char(string='Chart Url')
    luci_chart = fields.Text(compute='_compute_chart')

    @api.onchange('luci_chart_url')
    def _compute_chart(self):
        for rec in self:
            luci_chart = ''
            if rec.luci_chart_url:
                luci_chart = '<div style="width: 960px; height: 720px; margin: 10px; position: relative;"> ' \
                             '<iframe allowfullscreen="1" frameborder="0" style="width:1000px; height:720px" src="' + rec.luci_chart_url + '" id="MSKX7Jna2c80"></iframe>' \
                                                                                                                                           '</div>'
            rec.luci_chart = luci_chart
