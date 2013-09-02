# Adyengo

This is an Adyen app for Django. It provides an easy way to integrate the Adyen
payment system into a Django project. Regular, oneclick and recurring payments
are supported. All communication to and from Adyen is logged.

The project is however far from perfect and it hasn't been used in production
yet. There might be bugs, so be aware if you want to use this. Also, if you
use this app, you should still know how Adyen works, the app just simplifies
the process. However, occasionally the implementation documentation will
explain what happens under the hood. Sometimes it will refer to the Adyen
documentation for futher reading.


## Development

As said before, the project is far from perfect. Not all Adyen features are
implemented and the system hasn't even been tested thoroughly in production.
Since Adyen implementation is not straightforward and Adyen is a quite popular
payment service provider and Django is a popular framework, I hope people will
find use for it.

If you want to contribute, you're very welcome. Contact me for any questions.


## Installation

I haven't made a pip install for it yet, so you'll have to manually add it to
your project.


## Implementation

### Settings

To start out you should add some settings to your main `settings.py`.

#### Required settings

* `ADYEN_MERCHANT_ACCOUNT` - Your Adyen merchant account.
* `ADYEN_SHARED_SECRET` - The shared secret used to validate the communication with
    Adyen.
* `ADYEN_MODE` - Use `test` to use the Adyen test environment or `live` to use the
    live environment.

#### Required for Recurring Payments

* `WEB_SERVICES_USERNAME` - The username for the Adyen Web Services SOAP API.
* `WEB_SERVICES_PASSWORD` - The password for the Adyen Web Services SOAP API.
* `WEB_SERVICES_PUBLIC_KEY` - The public key for the Adyen Web Services SOAP API.

#### Optional settings

* `DEFAULT_SKIN_CODE` - The default skin code. Can always be overwritten.
* `DEFAULT_CURRENCY_CODE` - The default currency code. Can always be
    overwritten.

### Usage

There are two ways to do a payment through Adyen. One is to forward the
customer to the Adyen Hosted Payment Pages (HPP) and the other is to do an
Recurring Payment through Adyen's API.

Adyengo is reflects Adyen's interface in regular Django models and managers.
The main model to setup a payment is the `Session` model. Depending on what
kind of payment, you fill the fields of the `Session` model.

Most of the fields in the `Session` model reflect a field in the Adyen
interface. The only difference is that Adyen uses camelCase and Adyengo uses
under\_scores. So a field in the Adyen interface like `merchantReference` will
become `merchant_reference` in Adyengo. For information about these fields
please consult the Adyen Integration Manual.

Besides that, the `Session` model has some other fields for internal logic.

* `session_type` - The type of session. Choices are `hpp_regular`,
    `hpp_recurring` and `api_recurring`, but it is advised to use the
    constants for these variables, defined in `constants.py`.

    The constants for `session_type` are:

    * `SESSION_TYPE_HPP_REGULAR` - For a regular payment.
    * `SESSION_TYPE_HPP_RECURRING` - To setup a recurring contract, or to do a
        "oneclick" recurring payment.
    * `SESSION_TYPE_API_RECURRING` - For a recurring payment.

#### Regular payments

To set up a 

    from adyengo.models import Session
    from adyengo import constants

    s = Session(
        session_type=constants.SESSION_TYPE_HPP_REGULAR,
        merchant_reference=51391,
        payment_amount=1000,
        currency_code='EUR',
        ship_before_date=dateobject.isoformat(),
        skin_code='Nl0r8s5C',
        session_validity=dateobject.isoformat(),
        shopper_reference=13154,
        shopper_email='shopper@example.com',
        page_type=constants.PAGE_TYPE_MULTIPLE
    )
    s.save()
    params = s.params()
