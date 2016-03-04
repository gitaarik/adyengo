from django.conf import settings

# Your Adyen merchant account
MERCHANT_ACCOUNT = getattr(settings, 'ADYENGO_MERCHANT_ACCOUNT')

# The HMAC key used to validate the communication with Adyen
HMAC_KEY = getattr(settings, 'ADYENGO_HMAC_KEY')

# The mode the Adyen app will work in, either 'test' or 'live'
MODE = getattr(settings, 'ADYENGO_MODE', 'test')

# The default skin code. This option isn't required, but if it's not set, the
# system expects that the skin code will be provided when creating the session.
DEFAULT_SKIN_CODE = getattr(settings, 'ADYENGO_DEFAULT_SKIN_CODE', None)

# The default shopper locale. This option isn't required, but if it's not set, the
# system expects that the skin code will be provided when creating the session.
DEFAULT_SHOPPER_LOCALE = getattr(settings, 'ADYENGO_DEFAULT_SHOPPER_LOCALE', None)

# The default currency code. This option isn't required, but if it's not set,
# the system expects that the currency code will be provided when creating the
# session.
DEFAULT_CURRENCY_CODE = getattr(settings, 'ADYENGO_DEFAULT_CURRENCY_CODE', None)

DEFAULT_RES_URL = ''

API_USERNAME = getattr(settings, 'ADYENGO_API_USERNAME', None)
API_PASSWORD = getattr(settings, 'ADYENGO_API_PASSWORD', None)

if MODE == 'test':
    PAYMENT_PAGES_MULTIPLE_URL = 'https://test.adyen.com/hpp/select.shtml'
    PAYMENT_PAGES_SINGLE_URL = 'https://test.adyen.com/hpp/pay.shtml'
    PAYMENT_PAGES_SKIP_URL = 'https://test.adyen.com/hpp/details.shtml'
    PAYMENT_API_BASE_URL = 'https://pal-test.adyen.com/pal/servlet/Payment/v12/'
    RECURRING_API_BASE_URL = 'https://pal-test.adyen.com/pal/servlet/Recurring/v12/'

if MODE == 'live':
    PAYMENT_PAGES_MULTIPLE_URL = 'https://live.adyen.com/hpp/select.shtml'
    PAYMENT_PAGES_SINGLE_URL = 'https://live.adyen.com/hpp/pay.shtml'
    PAYMENT_PAGES_SKIP_URL = 'https://live.adyen.com/hpp/details.shtml'
    PAYMENT_API_BASE_URL = 'https://pal-live.adyen.com/pal/servlet/Payment/v12/'
    RECURRING_API_BASE_URL = 'https://pal-test.adyen.com/pal/servlet/Recurring/v12/'
