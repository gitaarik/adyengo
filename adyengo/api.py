import json
import requests
from . import settings


def exec_recurring_payment(
    contract_type,
    shopper_interaction,
    shopper_reference,
    shopper_email,
    merchant_reference,
    payment_amount,
    currency_code
):
    return payment_api_request(
        'authorise',
        {
            'amount': {
                'value': int(payment_amount),
                'currency': currency_code
            },
            'reference': merchant_reference,
            'merchantAccount': settings.MERCHANT_ACCOUNT,
            'shopperEmail': shopper_email,
            'shopperReference': shopper_reference,
            'selectedRecurringDetailReference': 'LATEST',
            'shopperInteraction': shopper_interaction,
            'recurring': {
                'contract': contract_type
            }
        }
    )


def list_recurring_details(shopper_reference, contract_type):
    return recurring_api_request(
        'listRecurringDetails',
        {
            'merchantAccount': settings.MERCHANT_ACCOUNT,
            'recurring': {
                'contract': contract_type
            },
            'shopperReference': shopper_reference
        }
    )


def disable_recurring_details(shopper_reference, recurring_detail_reference):
    return recurring_api_request(
        'disable',
        {
            'merchantAccount': settings.MERCHANT_ACCOUNT,
            'shopperReference': shopper_reference,
            'recurringDetailReference': recurring_detail_reference
        }
    )


def payment_api_request(endpoint, data):
    return api_request(
        '{}{}'.format(settings.PAYMENT_API_BASE_URL, endpoint),
        data
    )


def recurring_api_request(endpoint, data):
    return api_request(
        '{}{}'.format(settings.RECURRING_API_BASE_URL, endpoint),
        data
    )


def api_request(url, data):
    return requests.post(
        url,
        headers={'Content-Type': 'application/json'},
        auth=(settings.API_USERNAME, settings.API_PASSWORD),
        data=json.dumps(data)
    ).json()
