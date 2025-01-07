# -*- coding: utf-8 -*-
# controllers.py
import time

import json
import logging
from odoo import http
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
import requests
from odoo.http import request
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)

class MpesaController(http.Controller):


    

    @http.route('/mpesa/access_token', type='json', auth='public', methods=['POST'])
    def access_token(self):
        """Fetch MPesa access token from Safaricom API"""
        consumer_key = request.env.user.company_id.sudo().mpesa_consumer_key
        consumer_secret = request.env.user.company_id.sudo().mpesa_consumer_secret
        
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        # Fetch the token from Safaricom API
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        if r.status_code == 200:
            the_token = r.json().get('access_token')
            return {'access_token': the_token}
        else:
            _logger.error(f"Failed to get access token. Error: {r.text}")
            return {"error": "Failed to get access token"}



    def generate_callback_url(self, endpoint):
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            _logger.info(base_url+ endpoint)
            if base_url and base_url.startswith("http://"):
                base_url = base_url.replace("http://", "https://", 1)
                _logger.info(base_url+ endpoint)
                return base_url + endpoint
            return base_url + endpoint
            

    


    @http.route('/mpesa/stk_push', type='json', auth='public', methods=['POST'])
    def mpesa_stk_push(self, **kwargs):
        """Send the MPesa STK Push request using the access token"""
        access_token = kwargs.get('access_token')
        mpesa_phone_number = kwargs.get('phoneNumber')
        amount = kwargs.get('amount')
        _logger.info(f"Access Token: {access_token}")
        _logger.info(f"MPesa Phone Number: {mpesa_phone_number}")
        _logger.info(f"MPesa amount: {amount}")
        company_name = request.env.user.company_id.name


        # Save the transdetails


        if not access_token or not mpesa_phone_number:
            return {"error": "Missing access_token or mpesa_phone_number"}

        business_short_code = request.env.user.company_id.sudo().mpesa_shortcode

        
        
        callback_url = self.generate_callback_url('/custom_mpesa/callback')
        

        

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        payload = {
            "BusinessShortCode": business_short_code,
            "Password": self.generate_password(),
            "Timestamp": self.get_timestamp(),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": round(amount),
            "PartyA": mpesa_phone_number,
            "PartyB": business_short_code,
            "PhoneNumber": mpesa_phone_number,
            "CallBackURL": callback_url,
            "AccountReference": company_name,
            "TransactionDesc": "Payment of X"
        }
        response = requests.post(
            'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
            headers=headers,
            data=json.dumps(payload)
        )
        #update mpesa.request with response

        if response.status_code == 200:
            return response.json()
        else:
            return response.json()

       

    def generate_password(self):
        """Generate the MPesa password required for authentication"""
        pass_key = request.env.user.company_id.sudo().mpesa_passkey
        business_short_code = request.env.user.company_id.sudo().mpesa_shortcode
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f'{business_short_code}{pass_key}{timestamp}'.encode('utf-8')).decode('utf-8')
        return password

    def get_timestamp(self):
        """Get the current timestamp in the required format"""
        return datetime.now().strftime("%Y%m%d%H%M%S")
    


   


    @http.route('/mpesa/query', type='json', auth='public', methods=['POST'])
    def query_stk_status(self, **kwargs):
        """Query the status of an STK Push transaction."""
        checkout_request_id= kwargs.get('checkout_request_id')
        this_order = kwargs.get('thisOrder')
        access_token = self.access_token()
        if not access_token:
            raise UserError(_("Access token not found."))

        # query_url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"
        business_short_code = request.env.user.company_id.sudo().mpesa_shortcode
        timestamp = self.get_timestamp()
        # pass_key = request.env['ir.config_parameter'].sudo().get_param('pos.mpesa_passkey')
        password = self.generate_password()
        retry_count = 0
        max_retries = 5  # Limit the retries to avoid infinite loops
        delay_between_retries = 10 

        while retry_count < max_retries:
            try:
                bearer_token = access_token['access_token']

                response = requests.post(
                    "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query",
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {bearer_token}',
                    },
                    json={
                        'BusinessShortCode': business_short_code,
                        'Password': password,
                        'Timestamp': timestamp,
                        'CheckoutRequestID': checkout_request_id,
                    },
                )

                # Parse the response
                response_data = response.json()
                _logger.info(f"Response json: {response_data}")

                if response_data.get('errorCode') == '500.001.1001':
                    _logger.info("Transaction is still being processed. Retrying...")
                    retry_count += 1
                    time.sleep(delay_between_retries)  # Wait before retrying
                else:
                    pos_order = request.env['pos.order'].sudo().search([('pos_reference', '=', this_order)], limit=1)

                    
                    
                    # pos_order = request.env['pos.order'].sudo().search([
                    #     ('checkout_request_id', '=', checkout_request_id)
                    # ], limit=1)

                    if pos_order:
                        mpesa_receipt_number = 'SNMT0936T'
                        pos_order.write({'mpesa_receipt_number': mpesa_receipt_number})

                        _logger.info(pos_order)
                        _logger.info(f"Updated MPesa receipt number for order {pos_order.mpesa_receipt_number}.")
                    
                    return response_data



            except requests.exceptions.RequestException as e:
                _logger.error(f"Error querying STK status: {e}")
                break  # Exit on network failure or other request-related issues
        
        pos_order = request.env['pos.order'].sudo().search([('pos_reference', '=', this_order)], limit=1)
        _logger.warning(pos_order)
        if pos_order:
            # mpesa_receipt_number = 'SNMT0936T'
            # pos_order.write({'mpesa_receipt_number': mpesa_receipt_number})

            _logger.info(pos_order)
      
        _logger.info(f"Response for response: {response}")

        # response.raise_for_status()
        

        # return self.handle_query_response(response_data)

        # except requests.exceptions.RequestException as e:
        #     _logger.info(f"Error querying STK status: {requests.exceptions}")
        #     # raise UserError(_("Error querying STK status: %s") % str(e))
        # except json.JSONDecodeError as e:
        #     _logger.error(f"Error decoding JSON response: {e}")
            # raise UserError(_("Error decoding JSON response: %s") % str(e))

    def handle_query_response(self, response_data):
        """Handle the response from the STK query."""
        if 'ResultCode' in response_data:
            result_code = response_data['ResultCode']

            if result_code == '0':
                _logger.info("Transaction was successful. Proceeding to create payment record.")
                # return super(AccountPaymentRegister, self).action_create_payments()

            elif result_code == '1032':
                # Alert for Transaction Canceled by User
                _logger.warning("Transaction has been canceled by the user")
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Transaction Canceled'),
                        'message': _('The transaction has been canceled by the user.'),
                        'type': 'warning',
                        'sticky': True,
                        'next': {'type': 'ir.actions.act_window_close'},  # Action after closing
                    }
                }
            else:

              message = {
                '1037': "Timeout in completing transaction",
                # '1032': "Transaction has been canceled by the user",
                '1': "The balance is insufficient for the transaction"
            }.get(result_code, "Unknown result code: " + result_code)
            _logger.warning(message)
            # Return a notification to display on the UI
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Payment Failed'),
                    'message': str(message),
                    'type': 'danger',
                    'sticky': True,
                    # 'next': {'type': 'ir.actions.act_window_close'},  # Action after closing
                }
            }

        _logger.error("Error in response: No ResultCode found")
        return {
            'name': _('Error'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment.register',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'target': 'new',
            'context': {'warning': {'title': 'Error', 'message': "Unexpected response format."}},
        }



