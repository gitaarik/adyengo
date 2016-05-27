import base64
import binascii
import hashlib
import hmac
import ipaddress
from collections import OrderedDict
from . import settings, constants


def merchant_sig(params, clean_params=True):

    def clean_params(params):

        valid_params = (
            'allowedMethods', 'authResult', 'blockedMethods', 'brandCode',
            'countryCode', 'currencyCode', 'currencyCode', 'merchantAccount',
            'merchantReference', 'merchantReturnData', 'orderData',
            'paymentAmount', 'paymentMethod', 'pspReference',
            'recurringContract', 'resURL', 'selectedRecurringDetailReference',
            'sessionValidity', 'shipBeforeDate', 'shopperEmail',
            'shopperLocale', 'shopperReference', 'skinCode'
        )

        return {
            key: value
            for key, value in params.items()
            if key in valid_params
        }

    def remove_empty_values(params):
        return {
            key: value
            for key, value in params.items()
            if value is not None
        }

    if clean_params:
        params = clean_params(params)

    params = OrderedDict(sorted(remove_empty_values(params).items()))

    return calc_hmac(
        ':'.join(
            list(params.keys()) +
            escape_values(params.values())
        )
    )


def calc_hmac(string, hmac_key=settings.HMAC_KEY):
    return base64.encodestring(hmac.new(
        binascii.a2b_hex(hmac_key.encode()),
        string.encode(),
        hashlib.sha256
    ).digest()).strip().decode()


def escape_values(values):
    return [
        str(value).replace(r'\\', r'\\\\').replace(r':', r'\:')
        for value in values
    ]


def is_notification_item_hmac_valid(item):

    hmac_values = (
        item.get('pspReference', ''),
        item.get('originalReference', ''),
        item.get('merchantAccountCode', ''),
        item.get('merchantReference', ''),
        item.get('amount', {}).get('value', ''),
        item.get('amount', {}).get('currency', ''),
        item.get('eventCode'),
        item.get('success'),
    )

    hmac_signature = item.get('additionalData', {}).get('hmacSignature')

    if hmac_signature and hmac_signature == calc_hmac(
        ':'.join(escape_values(hmac_values)),
        settings.NOTIFICATION_HMAC_KEY
    ):
        return True


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_valid_ip(ip_address):
    for allowed_ip in constants.ADYEN_SERVERS_IP_ADDRESS_RANGES:
        if ipaddress.ip_address(ip_address) in ipaddress.ip_network(allowed_ip):
            return True
