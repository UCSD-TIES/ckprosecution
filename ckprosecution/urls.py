from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from ckprosecution import settings
from reports import *
from userena import views


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^home/','ckprosecution.views.home'),
    (r'^accounts/signup/', login_required(views.signup)),
    (r'^accounts/', include('userena.urls')),
    (r'^reports/', include('reports.urls')),
    # Examples:
    # url(r'^$', 'ckprosecution.views.home', name='home'),
    # url(r'^ckprosecution/', include('ckprosecution.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^$','accounts.views.landing'),
)
