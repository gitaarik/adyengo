import json
import dateutil.parser
from django.http import JsonResponse
from .models import Notification
from .utils import is_valid_ip, get_client_ip, is_notification_item_hmac_valid


class InvalidNotification(Exception):
    pass


class InvalidIp(InvalidNotification):
    pass


class HmacCalcInvalid(InvalidNotification):
    pass


def parse_notification(request):

    client_ip = get_client_ip(request)

    if not is_valid_ip(client_ip):
        raise InvalidIp('Invalid IP')

    data = json.loads(request.body.decode())

    def get_notification_items(data):
        return [
            i['NotificationRequestItem']
            for i in data.get('notificationItems', [])
        ]

    def save_notification_item(item):

        if not is_notification_item_hmac_valid(item):
            raise HmacCalcInvalid('HMAC calculation invalid')

        def adyen_bool(var):
            """
            Because Adyen likes to send strings where you expect bools..
            """
            if type(var) == bool:
                return var
            else:
                return var.lower() == 'true'

        def get_event_date():
            if item.get('eventDate'):
                return dateutil.parser.parse(item.get('eventDate'))

        amount = item.get('amount', {})

        # Adyen notificatins are likely to be sent twice, hence we use
        # `get_or_create()`.
        return Notification.objects.get_or_create(
            live=adyen_bool(data.get('live')),
            event_code=item.get('eventCode'),
            psp_reference=item.get('pspReference'),
            merchant_account_code=item.get('merchantAccountCode'),
            success=adyen_bool(item.get('success')),
            defaults={
                'ip_address': client_ip,
                'original_reference': item.get('originalReference'),
                'merchant_reference': item.get('merchantReference'),
                'event_date': get_event_date(),
                'payment_method': item.get('paymentMethod'),
                'operations': ','.join(item.get('operations', [])),
                'reason': item.get('reason'),
                'payment_amount': amount.get('value'),
                'currency_code': amount.get('currency')
            }
        )[0]  # `get_or_create()` returns `(obj, created)`, hence the `[0]`

    return [
        save_notification_item(item)
        for item in get_notification_items(
            json.loads(request.body.decode())
        )
    ]


def notification_valid_response():
    return JsonResponse({'notificationResponse': '[accepted]'})


def notification_invalid_response(error_message='Invalid Notification'):
    response = JsonResponse({'notificationResponse': error_message})
    response.status_code = 403
    return response
