from django.conf.urls import patterns, include, url
import accounts.views

urlpatterns = patterns('',
                       url(r'', include('django.contrib.auth.urls')),
                       url(r'^$', accounts.views.AccountList.as_view(), name='account_list'),
                       url(r'^new$', accounts.views.AccountCreate.as_view(), name='new_account'),
                       url(r'^(?P<slug>\w+)$', accounts.views.AccountDetail.as_view(), name='account_detail'),
                       url(r'^(?P<slug>\w+)/edit$', accounts.views.AccountUpdate.as_view(), name='account_edit'),
                       url(r'^(?P<slug>\w+)/delete$', accounts.views.AccountDelete.as_view(), name='account_delete'),
)
