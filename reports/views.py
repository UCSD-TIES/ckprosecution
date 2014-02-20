import csv
import json

from datetime import datetime

from django.core.urlresolvers import reverse_lazy

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from reports.models import Report

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
    if request.is_ajax():
        total_reports = Report.objects.all().count()

        response = []
        for creature in Report.objects.all().distinct('creature').values('creature'):
            c_string = creature['creature']
            response.append({'creature': c_string, 'count': Report.objects.filter(creature=c_string).count()})
        return HttpResponse(json.dumps(response), mimetype='application/json')
    else:
        return render_to_response('reports/statistics.html',
                                  context_instance=RequestContext(request))


class ReportList(ListView):
    model = Report
    context_object_name = 'reports'

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
