from django.conf.urls import patterns, include, url
import django.contrib.auth.urls
from django.contrib.auth.decorators import login_required
from ckprosecution import settings
from reports import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/', include('accounts.urls')),
    url(r'^reports/', include('reports.urls')),
    # Examples:
    # url(r'^$', 'ckprosecution.views.home', name='home'),
    # url(r'^ckprosecution/', include('ckprosecution.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','reports.views.plot_map')
)
