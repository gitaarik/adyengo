import uuid
import dateutil.parser

from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

from .models import (Session, SessionAllowedPaymentMethods,
    SessionBlockedPaymentMethods, Notification, RecurringContract)
from . import constants, settings, utils


def hpp_setup_session(request, session_type):

    if not session_type:
        session_type = constants.SESSION_TYPE_HPP_REGULAR

    tomorrow = (timezone.now() + timezone.timedelta(days=1))

    params = {
        'merchant_reference': uuid.uuid4(),
        'payment_amount': 1000,
        'currency_code': settings.DEFAULT_CURRENCY_CODE,
        'ship_before_date': tomorrow,
        'session_validity': tomorrow,
        'skin_code': settings.DEFAULT_SKIN_CODE,
        'shopper_reference': uuid.uuid4()
    }

    return render(request, 'adyengo/hpp/setup_session.html', {
        'session_type_hpp_regular': constants.SESSION_TYPE_HPP_REGULAR,
        'session_type_hpp_recurring': constants.SESSION_TYPE_HPP_RECURRING,
        'session_type': session_type,
        'currency_codes': constants.CURRENCY_CODES,
        'payment_methods': constants.PAYMENT_METHODS,
        'recurring_contract_types': constants.RECURRING_CONTRACT_TYPES_PLUS_COMBOS,
        'dispatch_url': reverse('adyengo:hpp_dispatch_session'),
        'params': params
    })


def hpp_dispatch_session(request):

    def p(p):
        # Get post parameter
        return request.POST.get(p, '')

    s = Session(
        session_type=p('session_type'),
        merchant_reference=p('merchant_reference'),
        payment_amount=p('payment_amount'),
        currency_code=p('currency_code'),
        ship_before_date=dateutil.parser.parse(p('ship_before_date')),
        skin_code=p('skin_code'),
        session_validity=dateutil.parser.parse(p('session_validity')),
        shopper_reference=p('shopper_reference'),
        shopper_email=p('shopper_email'),
        recurring_contract=p('recurring_contract'),
        page_type=p('page_type')
    )
    s.save()

    if request.POST.get('allowed_payment_methods'):
        for m in request.POST.getlist('allowed_payment_methods'):
            s.allowed_payment_methods.add(
                SessionAllowedPaymentMethods(method=m)
            )

    if request.POST.get('blocked_payment_methods'):
        for m in request.POST.getlist('blocked_payment_methods'):
            s.blocked_payment_methods.add(
                SessionBlockedPaymentMethods(method=m)
            )

    return render(request, 'adyengo/hpp/dispatch_session.html', {
        'url': s.url(),
        'params': s.hpp_params()
    })


def api_setup_request_contracts(request):
    return render(request, 'adyengo/api/setup_request_contracts.html', {
        'execute_url': reverse('adyengo:api_execute_request_contracts')
    })


def api_execute_request_contracts(request):

    contracts = RecurringContract.objects.contracts(
        request.POST.get('shopper_reference'),
        request.POST.get('contract_type')
    )

    return render(request, 'adyengo/api/execute_request_contracts.html', {
        'contracts': contracts
    })


def api_setup_recurring_session(request):

    params = {
        'merchant_reference': uuid.uuid4(),
        'selected_recurring_detail_reference': 'LATEST',
        'payment_amount': 1000,
        'currency_code': settings.DEFAULT_CURRENCY_CODE
    }

    return render(request, 'adyengo/api/setup_recurring_session.html', {
        'execute_url': reverse('adyengo:api_execute_recurring_session'),
        'params': params,
        'currency_codes': constants.CURRENCY_CODES,
        'recurring_contract_types': constants.RECURRING_CONTRACT_TYPES,
    })


def api_execute_recurring_session(request):

    def p(p):
        # Get post parameter
        return request.POST.get(p, '')

    s = Session(
        session_type=constants.SESSION_TYPE_API_RECURRING,
        merchant_reference=p('merchant_reference'),
        recurring_detail_reference=p('recurring_detail_reference'),
        recurring_contract=p('recurring_contract'),
        payment_amount=p('payment_amount'),
        currency_code=p('currency_code'),
        shopper_reference=p('shopper_reference'),
        shopper_email=p('shopper_email'),
        fraud_offset=int(p('fraud_offset')) if p('fraud_offset') else None,
        shopper_ip=p('shopper_ip'),
        shopper_statement=p('shopper_statement')
    )
    s.save()

    result = s.exec_recurring_payment()

    return render(request, 'adyengo/api/execute_recurring_session.html', {
        'result': result
    })


@csrf_exempt
def parse_notification(request):

    def p(p):
        # Get request parameter
        return request.REQUEST.get(p, '')

    n = Notification(
        ip_address=utils.get_client_ip(request),
        live=p('live'),
        event_code=p('eventCode'),
        psp_reference=p('pspReference'),
        original_reference=p('originalReference'),
        merchant_reference=p('merchantReference'),
        merchant_account_code=p('merchantAccountCode'),
        event_date=p('eventDate'),
        success=p('success'),
        payment_method=p('paymentMethod'),
        operations=p('operations'),
        reason=p('reason'),
        amount=p('amount')
    )

    if n.is_authorized():
        # authorized!
        pass
    else:
        # not authorized...
        pass

    return n.response()
