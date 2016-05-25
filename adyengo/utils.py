import binascii
import base64
import hmac
import hashlib
from collections import OrderedDict
from . import settings


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

    def get_field_values():
        return [
            str(value).replace(r'\\', r'\\\\').replace(r':', r'\:')
            for value in params.values()
        ]

    # this works
    return base64.encodestring(hmac.new(
        binascii.a2b_hex(settings.HMAC_KEY),
        ':'.join(
            list(params.keys()) +
            get_field_values()
        ).encode(),
        hashlib.sha256
    ).digest()).strip().decode()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
