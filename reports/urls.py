from django.conf.urls import patterns, include, url
from reports import views
from reports.views import ReportList, ReportCreate

urlpatterns = patterns('',
    url(r'^export_csv', 'reports.views.export_csv'),
    url(r'^statistics', 'reports.views.compute_statistics'),
    #url(r'^reports', 'reports.views.view_reports'),
    url(r'^$', ReportList.as_view(), name='report_list'),
    url(r'^add/$', ReportCreate.as_view(), name='report_add'),
    url(r'^search/$','reports.views.search'),
    url(r'^filter_by_date/$','reports.views.date_filter'),
    url(r'^report_(?P<report_id>\w+)','reports.views.detail', name="detail"),
    url(r'^deleted_report_(?P<report_id>\w+)','reports.views.delete_report', name="delete")
)
