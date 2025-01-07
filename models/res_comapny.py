from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'


    # Define fields for MPesa credentials
    mpesa_consumer_key = fields.Char(string="MPesa Consumer Key:")
    mpesa_consumer_secret = fields.Char(string="MPesa Consumer Secret:")
    mpesa_passkey = fields.Char(string="MPesa Passkey:")
    mpesa_shortcode = fields.Char(string="MPesa Shortcode:")