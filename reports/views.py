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
from django.db.models import Sum
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
        category = request.GET['gcat']
        response = []

        if(category == 'incidents_year'):
            for date_result in Report.objects.dates('crime_date', 'year'):
                year = date_result.year
                response.append({'name': year, 'count': Report.objects.filter(crime_date__year=year).count()})
        if(category == 'incidents_month'):
            months = {'01_Jan': 0, '02_Feb': 0, '03_Mar': 0, '04_Apr': 0, '05_May': 0, '06_Jun': 0, \
                      '07_Jul': 0, '08_Aug': 0, '09_Sep': 0, '10_Oct': 0, '11_Nov': 0, '12_Dec': 0}
            for q_result in Report.objects.all().values('crime_date'):
                month = q_result['crime_date'].month
                if(month == 1):
                    months['01_Jan'] += 1
                if(month == 2):
                    months['02_Feb'] += 1
                if(month == 3):
                    months['03_Mar'] += 1
                if(month == 4):
                    months['04_Apr'] += 1
                if(month == 5):
                    months['05_May'] += 1
                if(month == 6):
                    months['06_Jun'] += 1
                if(month == 7):
                    months['07_Jul'] += 1
                if(month == 8):
                    months['08_Aug'] += 1
                if(month == 9):
                    months['09_Sep'] += 1
                if(month == 10):
                    months['10_Oct'] += 1
                if(month == 11):
                    months['11_Nov'] += 1
                if(month == 12):
                    months['12_Dec'] += 1
            for item in months:
                response.append({'name': item, 'count': months[item]})
        if(category == 'num_suspects'):
            for q_result in Report.objects.all().distinct('num_involved').values('num_involved'):
                item = q_result['num_involved']
                response.append({'name': item, 'count': Report.objects.filter(num_involved=item).count()})
        if(category == 'resolve_days'):
            qs = {'0 - 10': 0, '10 - 19': 0, '20 - 29': 0, '30 - 39': 0, '40 - 49': 0, '>= 50': 0}
            for q_result in Report.objects.all().values('resolve_days'):
                days = q_result['resolve_days']
                if(days < 10):
                    qs['0 - 10'] += 1
                elif(10 <= days and days < 20):
                    qs['10 - 19'] += 1
                elif(20 <= days and days < 30):
                    qs['20 - 29'] += 1
                elif(30 <= days and days < 40):
                    qs['30 - 39'] += 1
                elif(40 <= days and days < 50):
                    qs['40 - 49'] += 1
                else:
                    qs['>= 50'] += 1
            for item in qs:
                response.append({'name': item, 'count': qs[item]})
        if(category == 'creature'):
            for q_result in Report.objects.all().distinct('creature').values('creature'):
                item = q_result['creature']
                response.append({'name': item, 'count': Report.objects.filter(creature=item).count()})
        if(category == 'location'):
            for q_result in Report.objects.all().distinct('location').values('location'):
                item = q_result['location']
                response.append({'name': item, 'count': Report.objects.filter(location=item).count()})
        if(category == 't_location'):
            for q_result in Report.objects.all().distinct('trial_location').values('trial_location'):
                item = q_result['trial_location']
                response.append({'name': item, 'count': Report.objects.filter(trial_location=item).count()})
        if(category == 'fine'):
            qs = {'0 - 100': 0, '100 - 199': 0, '200 - 299': 0, '300 - 399': 0, '400 - 499': 0, '>= 500': 0}
            for q_result in Report.objects.all().values('fine'):
                fine_val = q_result['fine']
                if(fine_val < 100):
                    qs['0 - 100'] += 1
                elif(100 <= fine_val and fine_val < 200):
                    qs['100 - 199'] += 1
                elif(200 <= fine_val and fine_val < 300):
                    qs['200 - 299'] += 1
                elif(300 <= fine_val and fine_val < 400):
                    qs['300 - 399'] += 1
                elif(400 <= fine_val and fine_val < 500):
                    qs['400 - 499'] += 1
                else:
                    qs['>= 500'] += 1
            for item in qs:
                response.append({'name': item, 'count': qs[item]})
        return HttpResponse(json.dumps(response), content_type='application/json')
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
