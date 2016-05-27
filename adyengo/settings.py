from django.conf import settings
from . import constants


adyengo_settings = getattr(settings, 'ADYENGO', {})

# Your Adyen merchant account
MERCHANT_ACCOUNT = adyengo_settings.get('MERCHANT_ACCOUNT', None)

# The HMAC key used to validate the communication with Adyen
HMAC_KEY = adyengo_settings.get('HMAC_KEY', None)

# The HMAC key used to validate notifications from Adyen
NOTIFICATION_HMAC_KEY = adyengo_settings.get('NOTIFICATION_HMAC_KEY', None)

# The mode the Adyen app will work in, either 'test' or 'live'
MODE = adyengo_settings.get('MODE', 'test')

# The default skin code. This option isn't required, but if it's not set, the
# system expects that the skin code will be provided when creating the session.
DEFAULT_SKIN_CODE = adyengo_settings.get('DEFAULT_SKIN_CODE', None)

# The default page type for an Adyen HPP (Hosted Payment Pages) payment
DEFAULT_PAGE_TYPE = adyengo_settings.get('DEFAULT_PAGE_TYPE', constants.PAGE_TYPE_MULTIPLE)

# The default shopper locale. This option isn't required, but if it's not set, the
# system expects that the skin code will be provided when creating the session.
DEFAULT_SHOPPER_LOCALE = adyengo_settings.get('DEFAULT_SHOPPER_LOCALE', None)

# The default currency code. This option isn't required, but if it's not set,
# the system expects that the currency code will be provided when creating the
# session.
DEFAULT_CURRENCY_CODE = adyengo_settings.get('DEFAULT_CURRENCY_CODE', None)

# The default URL the user gets redirected to after an Adyen HPP (Hosted
# Payment Pages) payment.
DEFAULT_RES_URL = adyengo_settings.get('DEFAULT_RES_URL', None)

# The credentials for the Adyen API
API_USERNAME = adyengo_settings.get('API_USERNAME', None)
API_PASSWORD = adyengo_settings.get('API_PASSWORD', None)

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
