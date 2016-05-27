import json
import dateutil.parser
from django.http import JsonResponse, HttpResponseForbidden
from django.db import IntegrityError
from .models import Notification
from .utils import is_valid_ip, get_client_ip, is_notification_item_hmac_valid


def parse_notification(request):

    if not is_valid_ip(get_client_ip(request)):
        return False

    data = json.loads(request.body)

    for item in data.get('notificationItems', []):

        if not is_notification_item_hmac_valid(item):
            return False

        def get_event_date():
            if item.get('eventDate'):
                return dateutil.parser.parse(item.get('eventDate'))

        amount = item.get('amount', {})

        n = Notification(
            live=data.get('live'),
            event_code=item.get('eventCode'),
            psp_reference=item.get('pspReference'),
            original_reference=item.get('originalReference'),
            merchant_reference=item.get('merchantReference'),
            merchant_account_code=item.get('merchantAccountCode'),
            event_date=get_event_date(),
            success=item.get('success'),
            payment_method=item.get('paymentMethod'),
            operations=','.join(item.get('operations', [])),
            reason=item.get('reason'),
            payment_amount=amount.get('value'),
            currency_code=amount.get('currency')
        )

        try:
            n.save()
        except IntegrityError:
            # Adyen notificatins are likely to be sent twice. Because of the
            # uniqueness on the fields, an `IntegrityError` is raised when the
            # same notification is trying to be inserted in the model. In this
            # case, we can ignore the notification (because we already
            # processed it).
            pass

    return True


def notification_valid_response():
    return JsonResponse({'notificationResponse': '[accepted]'})


def notification_invalid_response():
    return HttpResponseForbidden()
