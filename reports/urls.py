from django.conf.urls.defaults import *  # 404, 500, patterns, include, url

urlpatterns = patterns('',
    url(r'^statistics', 'reports.views.compute_statistics', name="compute_statistics"),
    url(r'^reports', 'reports.views.view_reports'),
    url(r'^search/$','reports.views.search'),
    url(r'^filter_by_date/$','reports.views.date_filter')
)
