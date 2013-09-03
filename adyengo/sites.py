from django.conf import settings
from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView


class AdyengoSite(object):

    @property
    def urls(self):

        if not settings.DEBUG:
            return

        urlpatterns = patterns('django.views.generic.simple',
            url(r'^$', RedirectView.as_view(url='hpp/setup_session/')),
        )

        urlpatterns += patterns('adyengo.views',

            url(r'^hpp/setup_session/((?P<session_type>\w+)/)?', 'hpp_setup_session', name='hpp_setup_session'),
            url(r'^hpp/dispatch_session/', 'hpp_dispatch_session', name='hpp_dispatch_session'),

            url(r'^api/setup_request_contracts/', 'api_setup_request_contracts', name='api_setup_request_contracts'),
            url(r'^api/execute_request_contracts/', 'api_execute_request_contracts', name='api_execute_request_contracts'),
            url(r'^api/setup_recurring_session', 'api_setup_recurring_session', name='api_setup_recurring_session'),
            url(r'^api/execute_recurring_session', 'api_execute_recurring_session', name='api_execute_recurring_session'),

            url(r'^notification/', 'parse_notification', name='parse_notification')

        )

        return urlpatterns, 'adyengo', 'adyengo'


site = AdyengoSite()
