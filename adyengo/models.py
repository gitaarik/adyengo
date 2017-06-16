from django.db import models
from django.utils import timezone

from .managers import RecurringContractManager
from .utils import remove_items_with_empty_values, merchant_sig
from . import settings, constants, api


def tomorrow():
    return (timezone.now() + timezone.timedelta(days=1))


class Session(models.Model):

    session_type = models.CharField(max_length=25, choices=sorted(constants.SESSION_TYPES.items()))
    merchant_reference = models.CharField(max_length=80, unique=True)
    payment_amount = models.PositiveSmallIntegerField()
    currency_code = models.CharField(
        max_length=3,
        choices=sorted(constants.CURRENCY_CODES.items()),
        default=settings.DEFAULT_CURRENCY_CODE
    )
    ship_before_date = models.DateTimeField(default=tomorrow, null=True)
    skin_code = models.CharField(max_length=10, default=settings.DEFAULT_SKIN_CODE)
    shopper_locale = models.CharField(
        max_length=5,
        choices=sorted(constants.LOCALES.items()),
        default=settings.DEFAULT_SHOPPER_LOCALE,
        blank=True
    )
    order_data = models.TextField(blank=True)
    session_validity = models.DateTimeField(default=tomorrow, null=True)
    merchant_return_data = models.CharField(max_length=128)
    country_code = models.CharField(max_length=2, choices=sorted(constants.COUNTRY_CODES.items()))
    shopper_email = models.EmailField(blank=True)
    shopper_reference = models.CharField(max_length=80, blank=True)
    shopper_ip = models.CharField(max_length=45, blank=True)
    shopper_statement = models.CharField(max_length=135, blank=True)
    fraud_offset = models.PositiveIntegerField(null=True)
    recurring_contract = models.CharField(
        max_length=50,
        choices=sorted(constants.RECURRING_CONTRACT_TYPES_PLUS_COMBOS.items()),
        blank=True
    )
    recurring_detail_reference = models.CharField(max_length=80, blank=True)
    res_url = models.CharField(max_length=2000, default=settings.DEFAULT_RES_URL, null=True, blank=True)
    page_type = models.CharField(
        max_length=15,
        choices=sorted(constants.PAGE_TYPES.items()),
        default=settings.DEFAULT_PAGE_TYPE
    )
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.merchant_reference

    class Meta:
        ordering = ('-creation_time',)

    def is_hpp_regular(self):
        return self.session_type == constants.SESSION_TYPE_HPP_REGULAR

    def is_hpp_recurring(self):
        return self.session_type == constants.SESSION_TYPE_HPP_RECURRING

    def is_api_recurring(self):
        return self.session_type == constants.SESSION_TYPE_API_RECURRING

    def url(self):

        if self.page_type == constants.PAGE_TYPE_MULTIPLE:
            return settings.PAYMENT_PAGES_MULTIPLE_URL

        if self.page_type == constants.PAGE_TYPE_SINGLE:
            return settings.PAYMENT_PAGES_SINGLE_URL

        if self.page_type == constants.PAGE_TYPE_SKIP:
            return settings.PAYMENT_PAGES_SKIP_URL

    def hpp_params(self):

        params = {
            'merchantReference': self.merchant_reference,
            'paymentAmount': self.payment_amount,
            'currencyCode': self.currency_code,
            'shipBeforeDate': self.ship_before_date.isoformat(),
            'skinCode': self.skin_code,
            'merchantAccount': settings.MERCHANT_ACCOUNT,
            'shopperLocale': self.shopper_locale,
            'orderData': self.order_data,
            'sessionValidity': self.session_validity.isoformat(),
            'merchantReturnData': self.merchant_return_data,
            'countryCode': self.country_code,
            'shopperEmail': self.shopper_email,
            'shopperReference': self.shopper_reference,
            'recurringContract': self.recurring_contract,
            'selectedRecurringDetailReference': self.recurring_detail_reference,
            'resURL': self.res_url,
            'allowedMethods': ','.join([
                m.method for m in self.allowed_payment_methods.all()
            ]),
            'blockedMethods': ','.join([
                m.method for m in self.blocked_payment_methods.all()
            ])
        }

        if self.page_type == constants.PAGE_TYPE_SKIP:
            params['brandCode'] = params['allowedMethods']

        params = remove_items_with_empty_values(params)
        params['merchantSig'] = merchant_sig(params)

        return params

    def exec_recurring_payment(self):
        """
        Executes the API call to Adyen to submit a recurring payment.

        Returns the result Adyen sends back as a dict with these keys:

        psp_reference       - The reference Adyen assigned to the payment. This
                              is guaranteed to be globally unique and must be
                              used when communicating about this payment with
                              Adyen.
        result_code         - The result of the payment. One of Authorised,
                              Refused or Error.
        auth_code           - An authorisation code if the payment was
                              successful, or blank otherwise.
        refusal_reason      - If the payment was refused, the refusal reason.
        """

        if self.recurring_contract == constants.RECURRING_CONTRACT_TYPE_RECURRING:
            shopper_interaction = 'ContAuth'
        elif self.recurring_contract == constants.RECURRING_CONTRACT_TYPE_ONECLICK:
            shopper_interaction = 'Ecommerce'

        # if self.fraud_offset:
        #     request['fraudOffset'] = self.fraud_offset

        # if self.shopper_statement:
        #     request['shopperStatement'] = self.shopper_statement

        # if self.shopper_ip:
        #     request['shopperIp'] = self.shopper_ip

        response = api.exec_recurring_payment(
            contract_type=self.recurring_contract,
            shopper_interaction=shopper_interaction,
            shopper_reference=self.shopper_reference,
            shopper_email=self.shopper_email,
            merchant_reference=self.merchant_reference,
            payment_amount=self.payment_amount,
            currency_code=self.currency_code
        )

        r = RecurringPaymentResult(
            session=self,
            psp_reference=response.get('pspReference'),
            result_code=response.get('resultCode'),
            auth_code=response.get('authCode'),
            refusal_reason=response.get('refusalReason', '')
        )
        r.save()

        return r

    def flush_recurring_contract_cache(self):
        """
        Flushes the Recurring Payment Contract cache we have for this
        shopper reference and contract type.

        This methods should be called when a session is authorized that
        potentially results in a new Recurring Payment Contract.

        We shouldn't try to refill the cache here right away, because sometimes
        there's a delay in the creation of the contracts at Adyen. Therefor
        it's best to always fetch the contracts from Adyen just before the
        payment.
        """
        # Split by comma because it can be a combination like
        # `ONECLICK,RECURRING`. In that case we want both contract types to be
        # flushed (because the potential new contract can be made for either).
        for c in self.recurring_contract.split(','):
            RecurringContract.objects.flush_cache(self.shopper_reference, c)


class SessionAllowedPaymentMethods(models.Model):

    session = models.ForeignKey(Session, related_name='allowed_payment_methods')
    method = models.CharField(max_length=50, choices=sorted(constants.PAYMENT_METHODS.items()))

    def __str__(self):
        return self.method


class SessionBlockedPaymentMethods(models.Model):

    session = models.ForeignKey(Session, related_name='blocked_payment_methods')
    method = models.CharField(max_length=50, choices=sorted(constants.PAYMENT_METHODS.items()))

    def __str__(self):
        return self.method


class RecurringContract(models.Model):

    recurring_detail_reference = models.CharField(max_length=150, blank=True)
    shopper_reference = models.CharField(max_length=80)
    contract_type = models.CharField(max_length=50)
    payment_method_type = models.CharField(max_length=15)
    variant = models.CharField(max_length=50, blank=True)
    creation_date = models.DateTimeField(blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)

    objects = RecurringContractManager()

    def __str__(self):
        return self.recurring_detail_reference

    class Meta:
        ordering = ('-creation_time',)
        unique_together = ('recurring_detail_reference', 'shopper_reference')

    @property
    def details_dict(self):
        """
        Returns a dict of the contract's details.
        """
        return {detail.key: detail.value for detail in self.details.all()}


class RecurringContractDetail(models.Model):

    recurring_contract = models.ForeignKey(RecurringContract, related_name='details')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.key


class RecurringPaymentResult(models.Model):

    session = models.ForeignKey(Session, related_name='recurring_payment_results')
    psp_reference = models.BigIntegerField()
    result_code = models.CharField(max_length=30, choices=sorted(constants.RECURRING_PAYMENT_RESULT_CODES.items()))
    auth_code = models.PositiveIntegerField(null=True)
    refusal_reason = models.CharField(max_length=250, blank=True)

    def is_authorized(self):
        return self.result_code == constants.RECURRING_PAYMENT_RESULT_AUTHORISED

    def is_received(self):
        return self.result_code == constants.RECURRING_PAYMENT_RESULT_RECEIVED

    def is_refused(self):
        return self.result_code == constants.RECURRING_PAYMENT_RESULT_REFUSED

    def is_error(self):
        return self.result_code == constants.RECURRING_PAYMENT_RESULT_ERROR


class Notification(models.Model):

    ip_address = models.CharField(max_length=45, null=True, blank=True)
    live = models.BooleanField()
    event_code = models.CharField(max_length=50, null=True, blank=True)
    psp_reference = models.CharField(max_length=150, null=True, blank=True)
    original_reference = models.CharField(max_length=150, null=True, blank=True)
    merchant_reference = models.CharField(max_length=128, null=True, blank=True)
    merchant_account_code = models.CharField(max_length=150, null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    success = models.BooleanField()
    payment_method = models.CharField(
        max_length=50,
        choices=sorted(constants.PAYMENT_METHODS.items()),
        null=True,
        blank=True
    )
    operations = models.CharField(max_length=100, null=True, blank=True)
    reason = models.CharField(max_length=250, null=True, blank=True)
    payment_amount = models.PositiveSmallIntegerField()
    currency_code = models.CharField(
        max_length=3,
        choices=sorted(constants.CURRENCY_CODES.items()),
        default=settings.DEFAULT_CURRENCY_CODE
    )
    session = models.ForeignKey(Session, null=True, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.event_code, self.psp_reference)

    def save(self, *args, **kwargs):

        # Try to find the session that initiated this notification. Generally,
        # this should always exist, but we don't want the notification to fail
        # in case it doesn't, therefor the `try` statement.
        try:
            self.session = Session.objects.get(
                merchant_reference=self.merchant_reference
            )
        except:
            pass

        super(Notification, self).save(*args, **kwargs)

        # If the session that this notification initiated was a HPP recurring
        # session, then the Recurring Contracts cache should be flushed.
        if self.session and self.session.is_hpp_recurring():
            self.session.flush_recurring_contract_cache()

    class Meta:
        ordering = ('-creation_time',)
        unique_together = ('live', 'merchant_account_code', 'psp_reference', 'event_code', 'success')

    def is_status(self, status_code):
        return (
            self.success and
            self.event_code == status_code
        )

    def is_authorized(self):
        return self.is_status(constants.NOTIFICATION_EVENT_CODE_AUTHORISATION)

    def is_cancelled(self):
        return self.is_status(constants.NOTIFICATION_EVENT_CODE_CANCELLATION)

    def is_refunded(self):
        return self.is_status(constants.NOTIFICATION_EVENT_CODE_REFUND)

    def is_canceled_or_refunded(self):
        return self.is_status(constants.NOTIFICATION_EVENT_CODE_CANCEL_OR_REFUND)

    def is_captured(self):
        return self.is_status(constants.NOTIFICATION_EVENT_CODE_CAPTURE)

    def is_refuned_reversed(self):
        return self.is_status(constants.NOTIFICATION_EVENT_CODE_REFUNDED_REVERSED)

    def is_capture_failed(self):
        return self.is_status(constants.NOTIFICATION_EVENT_CODE_CAPTURE_FAILED)

    def is_refund_failed(self):
        return self.is_status(constants.NOTIFICATION_EVENT_CODE_REFUND_FAILED)

    def is_request_for_information(self):
        return self.is_status(constants.NOTIFICATION_EVENT_CODE_REQUEST_FOR_INFORMATION)

    def is_notification_of_chargeback(self):
        return self.is_status(constants.NOTIFICATION_EVENT_CODE_NOTIFICATION_OF_CHARGEBACK)

    def is_advice_of_debit(self):
        return self.is_status(constants.NOTIFICATION_EVENT_CODE_ADVICE_OF_DEBIT)

    def is_chargedback(self):
        return self.is_status(constants.NOTIFICATION_EVENT_CODE_CHARGEBACK)

    def is_chargeback_reversed(self):
        return self.is_status(constants.NOTIFICATION_EVENT_CODE_CHARGEBACK_REVERSED)

    def is_report_available(self):
        return self.is_status(constants.NOTIFICATION_EVENT_CODE_REPORT_AVAILABLE)
