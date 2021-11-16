from odoo import api, fields, models
class PatientCardReport(models.AbstractModel):
    _name = 'report.doctorapiontement.action_patient_details'
    _description = 'Patient card Report'

    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     docs = self.env['hospital.patient'].browse(docids[0])
    #     appointments = self.env['hospital.appointment'].search([('patient_id', '=', docids[0])])
    #     appointment_list = []
    #     return {
    #         'doc_model': 'hospital.patient',
    #         'docs': docs,
    #         'appointment_list': appointment_list,
    #     }