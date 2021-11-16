from odoo import http

from odoo.http import request
import json as json


class Sale(http.Controller):

    @http.route('/patient_details', type='http', auth='public', website=True)
    def sale_details(self, **kwargs):
        sale_details = request.env['patient.form'].sudo().search([])
        return request.render('doctorapiontement.sale_details_page', {'my_details': sale_details})
        # return "hello"

    @http.route(['/doctor/form'], type='http', auth="public", website=True)
    def partner_form(self, **post):
        return request.render("doctorapiontement.tmp_customer_form", {})

    @http.route(['/doctor/form/submit'], method=['GET'], csrf=False, type='http', auth="public", website=True)
    def customer_form_submit(self, **post):
        partner = request.env['doctor.list'].create({
            'name': post.get('name'),
            'gender': post.get('gender'),
            'ph_no': post.get('ph_no')
        })
        vals = {
            'partner': partner,

        }
        data = {'message': 'success'}

        Data = json.dumps(data)
        return Data
        # return request.render("doctorapiontement.tmp_customer_form", vals)

    @http.route(['/doctor/form/delete'], type='http', auth="public", website=True)
    def _delete_from_db(self, **post):
        find_id = request.env['doctor.list'].search([('name', '=', post.get('name'))]).unlink()  # result demo.demo(1,)

        return request.render("doctorapiontement.tmp_delete_form_success")

    @http.route(['/doctor/form/search'], type='http', auth="public", website=True)
    def _search_from_db(self, **post):
        find_id = request.env['doctor.list'].search([('name', '=', post.get('name'))])

        return request.render("doctorapiontement.doctor_details_page", {'my_details': find_id})


class banner(http.Controller):

    @http.route('/doctorapiontement/banner', type='json', auth='user')
    def banner(self):
        return {
            'html': """
               <link>
               <center><h1><font color="red"> Patient List </font></h1></center>
               
      """
        }

    @http.route('/doctorapiontement/graph',  auth='user', website=True)
    def graph(self):
        return request.render('doctorapiontement.graph_template')


# class PartnerForm(http.Controller):
#
#     @http.route(['/doctor/form'], type='http', auth="public", website=True)
#
#     def partner_form(self, **post):
#         return request.render("doctorapiontement.tmp_customer_form", {})
#
#     @http.route(['/doctor/form/submit'], type='http', auth="public", website=True)
#
#     def customer_form_submit(self, **post):
#         partner = request.env['doctor.list'].create({
#             'name': post.get('name'),
#             'gender': post.get('gender'),
#             'ph_no': post.get('ph_no')
#         })
#         vals = {
#             'partner': partner,
#         }
#         return request.render("doctorapiontement.tmp_customer_form_success", vals)
#
#
#
# class deleteForm(http.Controller):
#
#         # @http.route(['/doctor/form'], type='http', auth="public", website=True)
#         # def partner_form(self, **post):
#         #     return request.render("doctorapiontement.tmp_customer_form", {})
#
#         @http.route(['/doctor/form/delete'], type='http', auth="public", website=True)
#         def _delete_from_db(self, **post):
#
#             find_id = request.env['doctor.list'].search([('name', '=', post.get('name'))]).unlink()  # result demo.demo(1,)
#
#             return request.render("doctorapiontement.tmp_delete_form_success")
#
#
# class searchForm(http.Controller):
#
#     @http.route(['/doctor/form/search'], type='http', auth="public", website=True)
#     def _search_from_db(self, **post):
#         find_id = request.env['doctor.list'].search([('name', '=', post.get('name'))])
#
#         return request.render("doctorapiontement.doctor_details_page", {'my_details': find_id})

# def customer_form_submit(self, **post):
#     partner = request.env['doctor.list'].sudo().search({
#         'name': post.get('name')
#
#     })
#
#     return  request.render('doctorapiontement.sale_details_page', {'my_details': partner})
# def sale_details(self, **kwargs):
#       sale_details = request.env['patient.form'].search(['name', '=', partner])
#       return request.render('doctorapiontement.sale_details_page', {'my_details': sale_details})


# def _search_from_db(self, **post):
#     find_id = request.env['doctor.list'].search([('name', '=', post.get('name'))])  # result demo.demo(1,)
#   vals ={
#     name = find_id.get('name'),
#     gender = find_id.get('gender'),
#     ph_no = find_id.get('ph_no')
#           }
#     return request.render("doctorapiontement.tmp_customer_form" )
