from odoo import api, fields, models,_
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

class pateint_form(models.Model):
    _name = 'patient.form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "patient_id desc"

    def name_get(self):
        # name get function for the model executes automatically
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.name, rec.patient_id)))
        return res

    @api.depends('birthdate')
    def _compute_age(self):
        for rec in self:
            if rec.birthdate:rec.age = (fields.date.today() - rec.birthdate) / timedelta(days=365.2425)


    #validation error is used to restrict value like age is not less then zero
    @api.constrains('age')
    def _age_check(self):
        for rec in self:
            if self.age <= 0:
                raise ValidationError("Please enter value greater than zero")

    name = fields.Char(string='Patient name', required=True, tracking=True, )
    ph_no = fields.Char(string=' Phone Number', track_visibility='always', size=10)
    address = fields.Char(string='Address')
    name_id = fields.Many2one('appointment.list')
    patient_id = fields.Char(string='Patient Id', required=True, copy=False, readonly=True,  default=lambda self: _('New'))
    # _sql_constraints = [('patient_id_unique', 'UNIQUE (patient_id)',
    #                      "The User ID must be unique, this one is already assigned to another user.")]
    birthdate = fields.Date(string=' Birthdate')
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')], required=True)
    blood_group = fields.Char('Blood Group')
    age = fields.Float(string="Age", compute=_compute_age, store=True)
    notes = fields.Char('Pervious History')
    reports = fields.Many2many('ir.attachment', string="Reports")
    doctor_name = fields.Many2one('doctor.list', string="Doctor")
    diagnosis_ids = fields.Many2many('patient.diagnosis')
    symptoms_ids = fields.Many2many('patient.symptoms')
    # image_medium =fields.Binary(attachment=True)
    admitted = fields.Boolean('Admitted or not')
    active = fields.Boolean(string='Active', default=True)
    room_id = fields.Many2one('room.list')
    user_signature = fields.Binary(string='Doctor Signature')
    wardname = fields.Char(related='room_id.ward_no')
    floorno = fields.Char(related='room_id.floor_no')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('created', 'Created'),
        ('confirm', 'Confirm'), ],  required=True, default='draft')

    def button_done(self):
        for rec in self:
            rec.write({'state': 'confirm'})
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'confirmed',
                    'type': 'rainbow_man',
                }
            }

    def button_reset(self):
        for rec in self:
            rec.state = 'draft'

    def button_cancel(self):
        for rec in self:
            rec.state = 'created'

    @api.model
    def create(self, vals):
        if vals.get('patient_id', _('New')) == _('New'):
            vals['patient_id'] = self.env['ir.sequence'].next_by_code('patient.form') or _('New')
            result = super(pateint_form, self).create(vals)
            return result

    @api.model
    def send_reminder(self):
        print("Create patient")


class doctor_list(models.Model):
    _name = 'doctor.list'
    # _inherits = {'hr.employee': 'employee_ids'}
    # _inherit = ['res.users']
    name = fields.Char("name")
    image_medium = fields.Binary("medium sized image", attachmen=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], required=True)
    # patient_name=fields.Many2one('patient.form')
    # apt_patient = fields.One2many('calendar.appointment.type','patient_name')
    ph_no = fields.Char('Phone Number')
    email = fields.Char('Email')
    # workinghours=fields.Datetime('select working hours')
    specialization = fields.Char('Specialization')
    user_id = fields.Many2one('res.users')
    active = fields.Boolean(string='Active', default=True)


class patient_wiz(models.TransientModel):
    _name = 'patient.wiz'
    patient_id = fields.Many2one('patient.form',string="Patient Name")

    def xls_report(self):
        # print("patient",self.read()[0])
        domain = []
        patient_id = self.patient_id
        if patient_id:
            domain += [('patient_id', '=', patient_id.patient_id)]
            print(domain)
        patient = self.env['patient.form'].search_read(domain)
        data = {
            'patient': patient,
            'form_data': self.read()[0]
        }
        # import pdb
        # pdb.set_trace()
        return self.env.ref('doctorapiontement.xls_report_down').report_action(self, data=data)



# class appointment_list(models.Model):
#     _name = 'appointment.list'
#     apt_date = fields.Date("Appointment Date")
#     apt_time = fields.Float(string="Time")
#     # patient_name = fields.Many2one('patient.form', string="patient Name")
#     patient_name = fields.Many2one('patient.form', string="patient Name")
#     dct_id = fields.Many2one('doctor.list')

class room_list(models.Model):
    _name = 'room.list'
    name = fields.Char('Ward name')
    floor_no = fields.Char('Floor No')
    ward_no = fields.Char("Room No")
    # room_ids = fields.One2many('patient.form', 'room_id')


class patient_diagnosis(models.Model):
    _name = 'patient.diagnosis'
    name = fields.Char()
    code = fields.Char("Diagnosis code")
    symptom_id = fields.Many2many('patient.symptoms')
    treatment_id = fields.Many2many('patient.treatment')
    notes = fields.Text()

class patient_symptoms(models.Model):
    _name = 'patient.symptoms'
    name = fields.Char()
    code = fields.Char("Symptom code")
    diagnosis = fields.Many2many('patient.diagnosis')
    note = fields.Text()

class bill_temp(models.Model):
    _inherit = 'account.payment'

    customer_name = fields.Char('Customer Name', required=True)
    seller_name = fields.Char('Seller Name')
    ph_no = fields.Char('Phone No')
    order_id = fields.Many2one('sale.order', string="Sale Order")
    amountfinal = fields.Monetary(string="Total Amount", related='order_id.amount_total')

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    patient_name = fields.Char(string='Patient Name')



class temp_product(models.Model):
  _inherit = 'product.template'
  treatment_ids = fields.Many2many('patient.treatment')

class patient_treatment(models.Model):
    _name = 'patient.treatment'
    name = fields.Char()
    code = fields.Char("Treatment code")
    treatment = fields.Many2many('patient.diagnosis')
    note = fields.Text()
    product_id = fields.Many2many('product.template')

class patient_appoint(models.Model):
    _inherit = 'calendar.appointment.type'
    orientation_compla = fields.Boolean("orientation compla")
    dct_name = fields.Many2many('doctor.list', string="Doctor Name")
    patient_name = fields.Many2one('patient.form', string="patient Name")

class PartnerXlsx(models.AbstractModel):
    _name = 'report.doctorapiontement.xls_report_down'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
         # print("mmsdf",data['patient'])
         sheet = workbook.add_worksheet('patient')
         # sheet.right_to_left()
         bold = workbook.add_format({'bold': True})
         sheet.set_column('D:D',12)
         sheet.set_column('E:E',13)
         row = 2
         col = 2
         sheet.write(row, col, 'Refrence', bold)

         sheet.write(row, col+1, 'patient Name', bold)
         sheet.write(row, col + 2, 'Phone No', bold)
         for patient in data['patient']:
            row += 1
            sheet.write(row, col, patient['patient_id'])

            sheet.write(row, col + 1, patient['name'])
            sheet.write(row, col + 2, patient['ph_no'])

        # for obj in partners:
        #     report_name = data['form_data']
        #     # One sheet by partner
        #     sheet = workbook.add_worksheet(report_name[:31])
        #     bold = workbook.add_format({'bold': True})
        #     sheet.write(0, 0, obj.name, bold)


