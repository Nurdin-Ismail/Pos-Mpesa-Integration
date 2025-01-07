# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class PosConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Fields related to the res.company model
    mpesa_consumer_key = fields.Char(
        related='company_id.mpesa_consumer_key',
        readonly=False
    )
    mpesa_consumer_secret = fields.Char(
        related='company_id.mpesa_consumer_secret',
        readonly=False
    )
    mpesa_passkey = fields.Char(
        related='company_id.mpesa_passkey',
        readonly=False
    )
    mpesa_shortcode = fields.Char(
        related='company_id.mpesa_shortcode',
        readonly=False
    )
    # mpesa_consumer_key = fields.Char(string="MPesa Consumer Key:")
    # mpesa_consumer_secret = fields.Char(string="MPesa Consumer Secret:")
    # mpesa_passkey = fields.Char(string="MPesa Passkey:")
    # mpesa_shortcode = fields.Char(string="MPesa Shortcode:")

    @api.depends('pos_config_id')
    def _compute_show_mpesa_config(self):
        active_payment_methods = self.env['pos.payment.method'].search([('active', '=', True)])
    
        # # Read only the 'id' and 'name' fields of active payment methods
        payment_data = active_payment_methods.read(['id', 'name'])

        # # Check if any active payment method's name contains 'mpesa'
        contains_mpesa = None

    # Check if any active payment method's name contains 'mpesa'
        for method in payment_data:
            if 'mpesa' in method['name'].lower():
                contains_mpesa = method['id']
                break  # Exit the loop once we find the first match
        
        if contains_mpesa:
            
            
            # Fetch all results as a list of tuples
            self.env.cr.execute("""
                SELECT pos_config_id, pos_payment_method_id
                FROM pos_config_pos_payment_method_rel
            """)
            
            # Fetch all results as a list of tuples
            relations = self.env.cr.fetchall()
            
            mpesa_pos_config_ids = [
                    relation[0] for relation in relations if relation[1] == contains_mpesa
                ]


            pos_config = self.env['pos.config'].search([], limit=1)  # Adjust search criteria as needed
            current_session_id = pos_config.current_session_id
            


            
            
            for rec in self:
                    for i in mpesa_pos_config_ids:
                        if str(i) in str(rec.pos_config_id):
                            rec.show_mpesa_config = i

            

            



        # for rec in self:
        #     rec.show_mpesa_config = self.pos_config_id

    show_mpesa_config = fields.Integer(compute='_compute_show_mpesa_config', store=True)


 

