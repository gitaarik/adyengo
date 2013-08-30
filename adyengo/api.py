from . import settings
from suds.client import Client


def recurring_soap_client():
    return adyen_soap_client(settings.RECURRING_SOAP_SERVICE_WSDL_URL)


def payment_soap_client():
    return adyen_soap_client(settings.PAYMENT_SOAP_SERVICE_WSDL_URL)


def adyen_soap_client(url):
    """
    Returns a suds (Python SOAP framework) client for the given url and adds
    Adyen specific credentials.
    """

    return Client(url,
        username=settings.WEB_SERVICES_USERNAME,
        password=settings.WEB_SERVICES_PASSWORD
    )
