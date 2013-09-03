from django.conf import settings

# Your Adyen merchant account
MERCHANT_ACCOUNT = getattr(settings, 'ADYENGO_MERCHANT_ACCOUNT')

# The shared secret used to validate the communication with Adyen
SHARED_SECRET = getattr(settings, 'ADYENGO_SHARED_SECRET')

# The mode the Adyen app will work in, either 'test' or 'live'
MODE = getattr(settings, 'ADYENGO_MODE', 'test')

# The default skin code. This option isn't required, but if it's not set, the
# system expects that the skin code will be provided when creating the session.
DEFAULT_SKIN_CODE = getattr(settings, 'ADYENGO_DEFAULT_SKIN_CODE', None)

# The default currency code. This option isn't required, but if it's not set,
# the system expects that the currency code will be provided when creating the
# session.
DEFAULT_CURRENCY_CODE = getattr(settings, 'ADYENGO_DEFAULT_CURRENCY_CODE', None)

WEB_SERVICES_USERNAME = getattr(settings, 'ADYENGO_WEB_SERVICES_USERNAME', None)
WEB_SERVICES_PASSWORD = getattr(settings, 'ADYENGO_WEB_SERVICES_PASSWORD', None)
WEB_SERVICES_PUBLIC_KEY = getattr(settings, 'ADYENGO_WEB_SERVICES_PUBLIC_KEY', None)

if MODE == 'test':
    PAYMENT_PAGES_MULTIPLE_URL = 'https://test.adyen.com/hpp/select.shtml'
    PAYMENT_PAGES_SINGLE_URL = 'https://test.adyen.com/hpp/pay.shtml'
    PAYMENT_PAGES_SKIP_URL = 'https://test.adyen.com/hpp/details.shtml'
    RECURRING_SOAP_SERVICE_WSDL_URL = 'https://pal-test.adyen.com/pal/Recurring.wsdl'
    PAYMENT_SOAP_SERVICE_WSDL_URL = 'https://pal-test.adyen.com/pal/Payment.wsdl'

if MODE == 'live':
    PAYMENT_PAGES_MULTIPLE_URL = 'https://live.adyen.com/hpp/select.shtml'
    PAYMENT_PAGES_SINGLE_URL = 'https://live.adyen.com/hpp/pay.shtml'
    PAYMENT_PAGES_SKIP_URL = 'https://live.adyen.com/hpp/details.shtml'
    RECURRING_SOAP_SERVICE_WSDL_URL = 'https://pal-live.adyen.com/pal/Recurring.wsdl'
    PAYMENT_SOAP_SERVICE_WSDL_URL = 'https://pal-live.adyen.com/pal/Payment.wsdl'
