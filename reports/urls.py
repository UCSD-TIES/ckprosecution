from django.conf.urls import patterns, include, url
from reports import views
from reports.views import ReportList, ReportCreate, ReportDetail, ReportUpdate, ReportDelete

urlpatterns = patterns('',
    url(r'^export_csv', 'reports.views.export_csv'),
    url(r'^statistics', 'reports.views.compute_statistics'),
    url(r'^$', ReportList.as_view(), name='report_list'),
    url(r'^add/$', ReportCreate.as_view(), name='report_add'),
    url(r'^search/$','reports.views.search'),
    url(r'^filter_by_date/$','reports.views.date_filter'),
    url(r'^report_(?P<pk>\w+)', ReportDetail.as_view(), name="report_detail"),
    url(r'^edit/(?P<pk>\d+)', ReportUpdate.as_view(), name='report_update'),
    url(r'^delete/(?P<pk>\w+)', ReportDelete.as_view(), name="report_delete")
)
