from django.core import urlresolvers
from django.contrib import admin
from .models import (
    Session, SessionAllowedPaymentMethods, SessionBlockedPaymentMethods,
    Notification, RecurringContract, RecurringContractDetail,
    RecurringPaymentResult
)


class SessionAllowedPaymentMethodsInline(admin.TabularInline):
    model = SessionAllowedPaymentMethods
    extra = 0


class SessionBlockedPaymentMethodsInline(admin.TabularInline):
    model = SessionBlockedPaymentMethods
    extra = 0


class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 0


class RecurringPaymentResultInline(admin.TabularInline):
    model = RecurringPaymentResult
    extra = 0


class SessionAdmin(admin.ModelAdmin):

    list_display = [
        'session_type', 'page_type', 'merchant_reference', 'payment_amount',
        'currency_code', 'shopper_locale', 'shopper_reference',
        'recurring_contract', 'creation_time'
    ]

    inlines = [
        SessionAllowedPaymentMethodsInline,
        SessionBlockedPaymentMethodsInline,
        NotificationInline,
        RecurringPaymentResultInline
    ]


class NotificationAdmin(admin.ModelAdmin):

    list_display = [
        'event_code', 'psp_reference', 'live', 'merchant_account_code',
        'payment_amount', 'currency_code', 'success', 'event_date', 'session',
        'creation_time'
    ]
    raw_id_fields = ['session']
    readonly_fields = ['session_link']

    def session_link(self, instance):

        if instance.session.id:
            change_url = urlresolvers.reverse(
                'admin:adyengo_session_change',
                args=(instance.session.id,)
            )

            return '<a class="changelink" href="{}">Session</a>'.format(change_url)

        else:
            return 'No related session found'

    session_link.allow_tags = True


class RecurringContractDetailInline(admin.TabularInline):
    model = RecurringContractDetail
    extra = 0


class RecurringContractAdmin(admin.ModelAdmin):
    list_display = [
        'recurring_detail_reference', 'shopper_reference', 'contract_type',
        'payment_method_type', 'variant', 'creation_date'
    ]
    inlines = (RecurringContractDetailInline,)


class RecurringPaymentResultAdmin(admin.ModelAdmin):

    list_display = ['session', 'psp_reference', 'result_code', 'auth_code']
    raw_id_fields = ['session']
    readonly_fields = ['session_link']

    def session_link(self, instance):

        if instance.session.id:
            change_url = urlresolvers.reverse(
                'admin:adyengo_session_change', args=(instance.session.id,)
            )

            return '<a class="changelink" href="{}">Session</a>'.format(change_url)

        else:
            return 'No related session found'

    session_link.allow_tags = True


admin.site.register(Session, SessionAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(RecurringContract, RecurringContractAdmin)
admin.site.register(RecurringPaymentResult, RecurringPaymentResultAdmin)
