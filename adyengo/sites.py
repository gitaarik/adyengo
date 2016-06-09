from django.conf import settings
from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views


class AdyengoSite(object):

    @property
    def urls(self):

        if not settings.DEBUG:
            raise Exception(
                "Please don't include Adyengo test page URL's when "
                "`DEBUG` is `False`."
            )

        urlpatterns = [
            url(r'^$', RedirectView.as_view(url='hpp/setup_session/')),
            url(r'^hpp/setup_session/((?P<session_type>\w+)/)?$', views.hpp_setup_session, name='hpp_setup_session'),
            url(r'^hpp/dispatch_session/$', views.hpp_dispatch_session, name='hpp_dispatch_session'),
            url(r'^hpp/result_page/$', views.hpp_result_page, name='hpp_result_page'),

            url(
                r'^api/setup_request_contracts/$',
                views.api_setup_request_contracts,
                name='api_setup_request_contracts'
            ),
            url(
                r'^api/execute_request_contracts/$',
                views.api_execute_request_contracts,
                name='api_execute_request_contracts'
            ),

            url(
                r'^api/setup_disable_recurring_contract/$',
                views.api_setup_disable_recurring_contract,
                name='api_setup_disable_recurring_contract'
            ),
            url(
                r'^api/execute_disable_recurring_contract/$',
                views.api_execute_disable_recurring_contract,
                name='api_execute_disable_recurring_contract'
            ),

            url(
                r'^api/setup_recurring_session/$',
                views.api_setup_recurring_session,
                name='api_setup_recurring_session'
            ),
            url(
                r'^api/execute_recurring_session/$',
                views.api_execute_recurring_session,
                name='api_execute_recurring_session'
            ),

            url(r'^notification/$', views.parse_notification, name='parse_notification')
        ]

        return urlpatterns, 'adyengo', 'adyengo'


site = AdyengoSite()
