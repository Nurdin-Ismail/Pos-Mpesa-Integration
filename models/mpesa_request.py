
from odoo import models, fields
import time

import json
import logging
from odoo import api, fields, models

from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
import requests
from odoo.http import request
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)


class MpesaRequest(models.Model):
    _name = 'mpesa.request'
    

    # order_id = models.manyToOne  link to the pos order
    # MerchantRequestID nullable
    # CheckoutRequestID nullable
    # Amount
    #Phone Number
