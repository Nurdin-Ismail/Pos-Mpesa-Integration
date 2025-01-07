# Mpesa POS Integration for Odoo

---

## Overview
This module integrates Mpesa payment functionality into Odoo's Point of Sale (POS) system. It enhances the payment process by enabling businesses to initiate Mpesa STK Push transactions directly from the POS interface and updates the user with the transaction status (**successful**, **canceled**, or **failed**).

---

## Features
- **Mpesa Configuration in Settings**: Manage Mpesa API credentials and settings in the Odoo Configuration menu.
- **Mpesa as a Payment Method**: Enable Mpesa as a payment method in the POS payment methods configuration.
- **STK Push Integration**: Send Mpesa STK Push requests when a phone number is entered on the POS numpad.
- **Real-Time Transaction Updates**: Receive and display updates on the transaction status within the POS interface.

---

## Requirements
- **Odoo version**: 17
- **Mpesa API**: Active Mpesa Daraja API account
- **Internet**: Required for API communication

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository_url> /path/to/odoo/addons/mpesa_pos
   ```
2. **Restart Odoo Server**:
   ```bash
   python3 odoo/odoo-bin -c config/odoo.conf
   ```
3. **Activate the Module in Odoo**:
   - Navigate to **Apps**.
   - Search for "Mpesa POS Integration."
   - Click **Install**.

---

## Configuration

### Step 1: Configure Mpesa API Parameters
1. Navigate to **Settings > Pos Settings > Mpesa Configuration**.
2. Fill in the following details:
   - **Consumer Key**
   - **Consumer Secret**
   - **Shortcode**
   - **Passkey**
   - **Callback URL**
3. Save the changes.

### Step 2: Enable Mpesa in POS
1. Go to **Point of Sale > Configuration > Payment Methods**.
2. Create or edit a payment method:
   - Set the name to **Mpesa**.
   - Assign the Mpesa configuration parameters.
3. Save the changes.

### Step 3: Assign Mpesa to POS Configurations
1. Go to **Point of Sale > Configuration > Point of Sale**.
2. Edit the POS configurations to include the Mpesa payment method.
3. Save the configuration.

---

## Usage

1. Open the **POS interface**.
2. Select **Mpesa** as the payment method.
3. Enter the customer’s **phone number** using the numpad.
4. Confirm to send the **STK Push request** to the customer’s phone.
5. Monitor the status of the transaction in real time:
   - **Success**: The transaction is completed and logged.
   - **Cancelled**: The user canceled the transaction.
   - **Failed**: An error occurred during the transaction.

---

## Development

### Key Components

- **Mpesa API Integration**:
  - Handles authentication, STK Push requests, and callbacks.
- **POS Frontend Customization**:
  - Adds phone number input and transaction status updates.
- **Configuration Management**:
  - Stores and validates Mpesa credentials in `res.config.settings`.

### Files and Directories
- `controllers/`: Contains custom controllers for handling API callbacks.
- `models/`: Defines Mpesa-related models and business logic.
- `views/`: Custom views for Mpesa configuration and POS interface enhancements.

---

## Testing

1. Ensure the **Callback URL** is accessible (use ngrok or port forwarding during development).
2. Test the following scenarios:
   - **Successful transaction**.
   - **Canceled transaction**.
   - **Failed transaction** due to invalid credentials or network issues.

---

## Troubleshooting

- **Callback Issues**:
  - Verify the Callback URL is reachable from Mpesa servers.
  - Check Odoo logs for detailed error messages.

- **STK Push Failures**:
  - Confirm the Mpesa API credentials are correctly configured.
  - Ensure the phone number entered is valid and registered with Mpesa.

---

