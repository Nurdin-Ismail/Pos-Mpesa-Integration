# POS MPesa Integration for Odoo

## Overview
This module integrates MPesa payment processing with the Odoo Point of Sale (POS) system. It allows seamless transactions between the POS application and the MPesa payment gateway, providing real-time updates on payment statuses and receipt generation.

## Features
- **STK Push Integration**: Initiate MPesa payments directly from the POS interface.
- **Real-time Status Checks**: Query and receive real-time feedback on the payment status.
- **Automatic Receipt Assignment**: Automatically associate MPesa receipts with POS orders.
- **Retry Mechanism**: Implements a retry loop for handling transactions that are pending or processing.
- **Secure Access**: Uses secure token-based authentication for API interactions.
- **Configurable Parameters**: Business shortcode and passkey can be set via Odoo configuration.

## Installation
1. **Clone this repository into your Odoo addons directory**:
   ```bash
   git clone https://github.com/yourusername/pos_mpesa_integration.git /path/to/odoo/addons/pos_mpesa_integration
    ```

2. **Restart your Odoo server**:

    ```bash
    ./odoo/odoo-bin -c /path/to/odoo.conf
    ```
3. **Navigate to Apps in your Odoo instance, search for "POS MPesa Integration," and install the module.**

**Configuration**


***POS Configuration:***

Assign the MPesa payment method to your POS sessions under Point of Sale > Configuration > Payment Methods.

![add](/static/description/add_mpesa.png)


***MPesa API Setup:***

1. Ensure that your MPesa API credentials (consumer key, consumer secret, passkey, and shortcode) are available.
2. Go to Settings > POint Of Sale Settings > MPesa Configuration to input these credentials.

![Configuration](/static/description/confuguration.png)


***Usage***
1. Open the POS session and select items for purchase.
2. Choose MPesa as the payment method.
3. Enter the customer's phone number and confirm the payment.
4. The system will initiate an STK Push to the customer's device.
5. Upon success, the transaction will be logged, and a receipt number will be linked to the order.


**Key Routes**

Initiate Payment:


    @http.route('/mpesa/stk_push',type='json', auth='public', methods=['POST'])

Query Payment Status:


    @http.route('/mpesa/query', type='json', auth='public', methods=['POST'])


**Technical Details**

**Dependencies:**

requests for handling HTTP requests.

Odoo's native HTTP controller for managing API endpoints.

***Authentication:***

1. Utilizes token-based authentication for secure MPesa API interactions.
2. Retry Logic: The module includes a retry mechanism for querying payment statuses.

**Error Handling**
1. Logs are written to the Odoo log file for troubleshooting.
2. Common errors such as expired tokens and connection issues are handled gracefully, with informative messages logged.

# Pos-Mpesa-Integration
