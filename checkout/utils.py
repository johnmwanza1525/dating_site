import requests
import logging
from dating_app import local_settings as l_s
# Initialize a logger
logger = logging.getLogger(__name__)

DARJA_API_BASE_URL = "https://sandbox.safaricom.co.ke"
CONSUMER_KEY = l_s.MPESA_CONSUMER_KEY
CONSUMER_SECRET = l_s.MPESA_CONSUMER_SECRET
LIPA_NA_MPESA_SHORTCODE = l_s.MPESA_SHORTCODE
LIPA_NA_MPESA_PASSKEY = l_s.MPESA_PASSKEY


def get_mpesa_access_token():
    response = requests.get(
        f"{DARJA_API_BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
        auth=(CONSUMER_KEY, CONSUMER_SECRET)
    )
    return response.json().get('access_token')

def initiate_mpesa_payment(amount, phone_number, reference, description):
    access_token = get_mpesa_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "BusinessShortCode": LIPA_NA_MPESA_SHORTCODE,
        "Password": get_mpesa_password(),
        "Timestamp": get_mpesa_timestamp(),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": LIPA_NA_MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://ea67-105-160-102-24.ngrok-free.app/mpesa-callback/",
        "AccountReference": reference,
        "TransactionDesc": description
    }
    response = requests.post(
        f"{DARJA_API_BASE_URL}/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers=headers
    )
    return response.json()

def verify_mpesa_payment(order_id):
    access_token = get_mpesa_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Use the order_id as a unique identifier to track the payment status
    payload = {
        "BusinessShortCode": LIPA_NA_MPESA_SHORTCODE,
        "Password": get_mpesa_password(),
        "Timestamp": get_mpesa_timestamp(),
        "CheckoutRequestID": order_id
    }

    response = requests.post(
        f"{DARJA_API_BASE_URL}/mpesa/stkpushquery/v1/query",
        json=payload,
        headers=headers
    )

    # Debug: log the response for troubleshooting
    logger.info(f"M-Pesa payment verification response: {response.json()}")

    if response.status_code == 200:
        result = response.json()
        if result.get("ResultCode") == "0":
            return "Completed"
        else:
            return "Failed"
    else:
        logger.error(f"Failed to verify M-Pesa payment: {response.status_code} - {response.text}")
        return "Failed"


def get_mpesa_password():
    import base64
    from datetime import datetime

    data = LIPA_NA_MPESA_SHORTCODE + LIPA_NA_MPESA_PASSKEY + get_mpesa_timestamp()
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')

def get_mpesa_timestamp():
    from datetime import datetime
    return datetime.now().strftime('%Y%m%d%H%M%S')
