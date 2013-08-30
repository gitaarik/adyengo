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

To start out you should add some settings to your main `settings.py`. The
following settings are required:

* `MERCHANT_ACCOUNT` - Your Adyen merchant account.
* `SHARED_SECRET` - The shared secret used to validate the communication with
                    Adyen.
* `MODE` - Either `test` or `live`, will determine which Adyen system will be
           used.

// In progress...
