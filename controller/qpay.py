import requests
import json
from datetime import datetime


def accessToken():
    url = "https://merchant.qpay.mn/v2/auth/token"
    payload = ""
    headers = {
        'Authorization': 'Basic'
    }

    response = requests.request("POST", url, headers=headers, data=payload, auth=('GMOBILE', 'E0wGvjHG'))
    if 'access_token' in response.json():
        access_token = response.json()['access_token']
    else:
        access_token = ""
    return access_token


def refreshToken():
    url = "https://merchant.qpay.mn/v2/auth/refresh"
    payload = {}
    headers = {
        'Authorization': 'Bearer '
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    refresh_token = response.json()['refresh_token']
    return refresh_token


def invoice(order_id, product_name, amount):
    access_token = accessToken()
    url = "https://merchant.qpay.mn/v2/invoice"

    payload = json.dumps({
        "invoice_code": "GMOBILE_INVOICE",
        "sender_invoice_no": order_id,
        "invoice_receiver_code": "terminal",
        "invoice_description": product_name,
        "amount": amount,
        "callback_url": "https://kiosk.gmobile.mn/api/callBackUrl?payment_id={0}".format(order_id)
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def check_qpay(invoice_id):
    access_token = accessToken()
    url = "https://merchant.qpay.mn/v2/payment/check"

    payload = json.dumps({
        "object_type": "INVOICE",
        "object_id": invoice_id
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token,
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()
