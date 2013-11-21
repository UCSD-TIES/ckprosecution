from django.conf.urls.defaults import *  # 404, 500, patterns, include, url

urlpatterns = patterns('',
    url(r'^export_csv', 'reports.views.export_csv'),
    url(r'^statistics', 'reports.views.compute_statistics'),
    url(r'^reports', 'reports.views.view_reports'),
    url(r'^search/$','reports.views.search'),
    url(r'^filter_by_date/$','reports.views.date_filter'),
    url(r'^rank_by_(?P<rank_by>\w+)_reverse=(?P<reverse>\w+)','reports.views.rank', name="rank"),
    url(r'^report_(?P<report_id>\w+)','reports.views.detail', name="detail"),
    url(r'^deleted_report_(?P<report_id>\w+)','reports.views.delete_report', name="delete")
)
