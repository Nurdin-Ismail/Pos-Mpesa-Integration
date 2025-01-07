# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class PosConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Define fields for MPesa credentials
    mpesa_consumer_key = fields.Char(string="MPesa Consumer Key:")
    mpesa_consumer_secret = fields.Char(string="MPesa Consumer Secret:")
    mpesa_passkey = fields.Char(string="MPesa Passkey:")
    mpesa_shortcode = fields.Char(string="MPesa Shortcode:")

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
            
            # the_match = self.pos_config_id
            # numb = the_match

            # if numb in mpesa_pos_config_ids:
            #     the_match = numb
            
            # if numb in mpesa_pos_config_ids:
            #     for rec in self:
            #         rec.show_mpesa_config = self.pos_config_id

            # the_match = self.pos_config_id
            #     numb = the_match


                
            #     if numb in mpesa_pos_config_ids:
            #         for rec in self:
            #             rec.show_mpesa_config = self.pos_config_id

            pos_config = self.env['pos.config'].search([], limit=1)  # Adjust search criteria as needed
            current_session_id = pos_config.current_session_id
            

                # if self.pos_config_id in mpesa_pos_config_ids:
            
            
            for rec in self:
                    for i in mpesa_pos_config_ids:
                        if str(i) in str(rec.pos_config_id):
                            rec.show_mpesa_config = i

            

            



        # for rec in self:
        #     rec.show_mpesa_config = self.pos_config_id

    show_mpesa_config = fields.Integer(compute='_compute_show_mpesa_config', store=True)


 


    def print_chosen_payment_methods(self):
        pos_configs = self.env['pos.config'].search([])
        for config in pos_configs:
            print(f"POS Configuration: {config.name}")
            for method in config.pos_payment_method_ids:
                print(f"Payment Method: {method.name}")

    @api.model
    def get_values(self):
        # Retrieve MPesa settings from system parameters
        res = super(PosConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            mpesa_consumer_key=params.get_param('pos.mpesa_consumer_key', default=''),
            mpesa_consumer_secret=params.get_param('pos.mpesa_consumer_secret', default=''),
            mpesa_passkey=params.get_param('pos.mpesa_passkey', default=''),
            mpesa_shortcode=params.get_param('pos.mpesa_shortcode', default=''),
        )
        return res

    def set_values(self):
        # Save MPesa settings to system parameters
        super(PosConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('pos.mpesa_consumer_key', self.mpesa_consumer_key or '')
        params.set_param('pos.mpesa_consumer_secret', self.mpesa_consumer_secret or '')
        params.set_param('pos.mpesa_passkey', self.mpesa_passkey or '')
        params.set_param('pos.mpesa_shortcode', self.mpesa_shortcode or '')

