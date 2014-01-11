import os
import csv
from datetime import datetime
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils import simplejson
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.context_processors import csrf
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from reports.models import Report
from reports.forms import ReportForm
from reports.search import *

from GChartWrapper import *

"""This function exports all the data to a csv file titled with the timestamp"""


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    #get the timestamp
    i = datetime.now()
    #format the timestamp and string append to filename
    filename = i.strftime('%Y%m%d%H%M') + '.csv'
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    writer = csv.writer(response)
    #write the row of all the fields
    writer.writerow(
        ['Crime Date', 'Resolve Days', 'Suspects', 'Creature', 'Location', 'Trial Location', 'Violation Description',
         'Fine', 'Jail', 'MPA', 'Update Date'])

    #write all rows in database using loop
    for row in Report.objects.all():
        rcrime_date = '' + str(row.crime_date)
        rresolve_days = '' + str(row.resolve_days)
        rnum_involved = '' + str(row.num_involved)
        rcreature = '' + str(row.creature)
        rlocation = '' + str(row.location)
        rtrial_location = '' + str(row.trial_location)
        rviolation_description = '' + str(row.violation_description)
        rfine = '' + str(row.fine)
        rupdate_date = '' + str(row.update_date)
        rjail_time = '' + str(row.jail_time)
        rmpa = '' + str(row.mpa)
        writer.writerow(
            [rcrime_date, rresolve_days, rnum_involved, rcreature, rlocation, rtrial_location, rviolation_description,
             rfine, rjail_time, rmpa, rupdate_date])

    return response


@login_required
def compute_statistics(request):
    total_reports = Report.objects.all().count()

    # Start of Graph

    ## Resolve days graph ##
    days_stats_label = ""
    count_stats_label = ""
    days_stats_data = []
    for resolve_days in Report.objects.all().distinct('resolve_days').values('resolve_days'):
        c_string = '' + str(resolve_days).lstrip("{'resolve_days': u'").rstrip("'{}")
        count = float(Report.objects.filter(resolve_days=c_string).count())
        count_stats_label += str(Report.objects.filter(resolve_days=c_string).count())
        days_stats_label += str(c_string) + "|"
        days_stats_data.append(count)
    roof = max(list(map(int, count_stats_label)))
    days_graph = VerticalBarStack(days_stats_data)
    days_graph.title('Frequency of Resolve Days')
    days_graph.bar(500 / days_stats_label.count("|"), 100 / days_stats_label.count("|"), 0)
    days_graph.size(600, 300)
    days_graph.axes.type('xyx')
    {}
    days_graph.axes.range(1, 0, roof, 1)
    days_graph.axes.label(2, 'Number of Days to Resolve')
    days_graph.axes.position(2, 50)
    ##days_graph.axes.label(1,'Occurrence')
    days_graph.scale(0, roof)
    days_graph.label(days_stats_label.rstrip("|"))
    days_graph.color('0000aa')

    ##Date Graph
    ## code to replace place-holder when report format for crime_date is fixed
    ## need to extract just the year from the data
    ## Date Line Graph##
    ##date_stats_label = ""
    ##count_stats_label = ""
    ##date_stats_data = []
    ##for crime_date in Report.objects.all().distinct('crime_date').values('crime_date'):
    ##c_string = '' + str(crime_date).lstrip("{'update_date': u'").rstrip("'{}}")
    ##count = float(Report.objects.filter(crime_date=c_string).count())
    ##count_stats_label += str(Report.objects.filer(resolve_Days=c_string).count())
    ##date_stats_label += str(c_string) + "|"
    ##date_stats_data.append(count)
    ##roof = max(list(map(int, count_stats_label)))
    ##date_graph = Line(date_stats_data)
    date_graph = Line([0, 4, 2, 9, 1, 2])
    date_graph.title('Violations by Year')
    date_graph.size(600, 300)
    date_graph.axes.type('xyx')
    {}
    ##date_graph.label(date_stats_label).rstrip("|")
    date_graph.axes.range(1, 0, 9, 1)
    date_graph.axes.label(2, 'Year')
    date_graph.axes.position(2, 50)
    date_graph.scale(0, 9)
    date_graph.label(2008, 2009, 2010, 2011, 2012, 2013)
    date_graph.color('0000aa')
    ## Location of Violations##
    location_stats_label = ""
    location_stats_data = []

    for location in Report.objects.all().distinct('location').values('location'):
        c_string = '' + str(location).lstrip("{'location': u'").rstrip("'}")
        percentage = (float(Report.objects.filter(location=c_string).count()) / total_reports) * 100
        location_stats_label += str(c_string) + " " + str(round(percentage, 2)) + "%|"
        location_stats_data.append(percentage)

    location_graph = Pie(location_stats_data)
    location_graph.title('Total Violations by Location XXXXX')
    location_graph.size(600, 300)
    location_graph.label(location_stats_label.rstrip("|"))
    location_graph.color('0000aa')

    ## Creatures Affected by Violations ##
    creature_stats_label = ""
    creature_stats_data = []

    for creature in Report.objects.all().distinct('creature').values('creature'):
        c_string = '' + str(creature).lstrip("{'creature': u'").rstrip("'}")
        percentage = (float(Report.objects.filter(creature=c_string).count()) / total_reports) * 100
        creature_stats_label += str(c_string) + " " + str(round(percentage, 2)) + "%|"
        creature_stats_data.append(percentage)

    creature_graph = Pie(creature_stats_data)
    creature_graph.title('Creatures Affected by Violations')
    creature_graph.size(600, 300)
    creature_graph.label(creature_stats_label.rstrip("|"))
    creature_graph.color('0000aa')

    #End of graphs

    return render_to_response('reports/statistics.html', {
        'date_graph': date_graph,
        'creature_graph': creature_graph,
        'days_graph': days_graph},
                              context_instance=RequestContext(request))


class ReportList(ListView):
    model = Report
    context_object_name = 'reports'

    def get_queryset(self):
        if self.request.GET.get('start_date'):
            start_date = self.request.GET.get('start_date')
        if self.request.GET.get('end_date'):
            end_date = self.request.GET.get('end_date')
            return Report.objects.filter(crime_date__range=[start_date, end_date])

        return Report.objects.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReportList, self).dispatch(*args, **kwargs)


class ReportCreate(CreateView):
    model = Report
    success_url = reverse_lazy('report_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReportCreate, self).dispatch(*args, **kwargs)


class ReportDetail(DetailView):
    model = Report

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReportDetail, self).dispatch(*args, **kwargs)


class ReportUpdate(UpdateView):
    model = Report

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReportUpdate, self).dispatch(*args, **kwargs)


class ReportDelete(DeleteView):
    model = Report
    success_url = reverse_lazy('report_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReportDelete, self).dispatch(*args, **kwargs)


@login_required
def plot_map(request):
    return render_to_response('map.html', {
        'reports': Report.objects.all()},
                              context_instance=RequestContext(request))
