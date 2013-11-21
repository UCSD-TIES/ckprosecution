import os
import csv
from datetime import datetime 
from django.utils import simplejson
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.context_processors import csrf
from django.views.decorators.csrf import requires_csrf_token

from reports.models import Report
from reports.forms import ReportForm
from reports.search import *

from GChartWrapper import *


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    i = datetime.now()
    filename = i.strftime('%Y%m%d%H%M') + '.csv'
    response['Content-Disposition'] = 'attachment; filename="'+ filename +'"'

    writer = csv.writer(response)
    writer.writerow(['Crime Date', 'Resolve Days', 'Suspects', 'Creature', 'Location', 'Trial Location', 'Violation Description' , 'Fine', 'Jail', 'MPA', 'Update Date'])

    for row in Report.objects.all():
        rcrime_date = '' + str(row.crime_date)
	rresolve_days = ''+str(row.resolve_days) 
	rnum_involved = ''+str(row.num_involved) 
	rcreature = ''+str(row.creature) 
	rlocation = ''+str(row.location) 
	rtrial_location = ''+str(row.trial_location) 
	rviolation_description = ''+str(row.violation_description) 
	rfine = ''+str(row.fine) 
	rupdate_date = ''+str(row.update_date) 
	rjail_time = ''+str(row.jail_time) 
	rmpa = ''+str(row.mpa) 
        writer.writerow([rcrime_date, rresolve_days, rnum_involved, rcreature, rlocation, rtrial_location, rviolation_description, rfine, rjail_time, rmpa, rupdate_date])

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
    days_graph.bar(500/days_stats_label.count("|"),100/days_stats_label.count("|"),0)
    days_graph.size(600,300)
    days_graph.axes.type('xyx')
    {}
    days_graph.axes.range(1,0,roof,1)
    days_graph.axes.label(2,'Number of Days to Resolve')
    days_graph.axes.position(2, 50)
    ##days_graph.axes.label(1,'Occurrence')
    days_graph.scale(0,roof)
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
    date_graph = Line([0,4,2,9,1,2])
    date_graph.title('Violations by Year')
    date_graph.size(600,300)
    date_graph.axes.type('xyx')
    {}
    ##date_graph.label(date_stats_label).rstrip("|")
    date_graph.axes.range(1,0,9,1)
    date_graph.axes.label(2,'Year')
    date_graph.axes.position(2,50)
    date_graph.scale(0,9)
    date_graph.label(2008,2009,2010,2011,2012,2013)
    date_graph.color('0000aa')
    ## Location of Violations##
    location_stats_label = ""
    location_stats_data = []

    for location in Report.objects.all().distinct('location').values('location'):
        c_string = '' + str(location).lstrip("{'location': u'").rstrip("'}")
        percentage = (float(Report.objects.filter(location=c_string).count()) / total_reports) * 100
        location_stats_label+= str(c_string) + " " + str(round(percentage, 2)) + "%|"
        location_stats_data.append(percentage)

    location_graph = Pie(location_stats_data)
    location_graph.title('Total Violations by Location XXXXX')
    location_graph.size(600,300)
    location_graph.label(location_stats_label.rstrip("|"))
    location_graph.color('0000aa')

    ## Creatures Affected by Violations ##
    creature_stats_label = ""
    creature_stats_data = []

    for creature in Report.objects.all().distinct('creature').values('creature'):
        c_string = '' + str(creature).lstrip("{'creature': u'").rstrip("'}")
        percentage = (float(Report.objects.filter(creature=c_string).count()) / total_reports) * 100
        creature_stats_label+= str(c_string) + " " + str(round(percentage, 2)) + "%|"
        creature_stats_data.append(percentage)

    creature_graph = Pie(creature_stats_data)
    creature_graph.title('Creatures Affected by Violations')
    creature_graph.size(600,300)
    creature_graph.label(creature_stats_label.rstrip("|"))
    creature_graph.color('0000aa')

    #End of graphs

    return render_to_response('reports/statistics.html', {
                              'date_graph': date_graph,
                              'creature_graph': creature_graph,
                              'days_graph': days_graph},
                              context_instance=RequestContext(request))

from reports.forms import ReportForm

@login_required
def view_reports(request):
    formset = ReportForm()
    if request.method == 'POST':
        if request.POST.get('report'):
            report = get_object_or_404(Report, pk=request.POST.get('report'))
            form = ReportForm(request.POST, instance=report)
            if form.is_valid():
                report = form.save()
                report.save()
                return render_to_response('reports/reports.html',{
                                          'success': "success",
                                          'form': formset,
                                          'reports': Report.objects.all()},
                                          context_instance=RequestContext(request))
            else:
                return render_to_response('reports/reports.html',{
                                          'error': form.errors,
                                          'form': formset,
                                          'reports': Report.objects.all()},
                                          context_instance=RequestContext(request))
        else:
            form = ReportForm(request.POST)
            if form.is_valid():
                new_report= form.save()
                return render_to_response('reports/reports.html',{
                                          'success': "success",
                                          'form': formset,
                                          'reports': Report.objects.all()},
                                          context_instance=RequestContext(request))
            else:
                return render_to_response('reports/reports.html',{
                                          'error': form.errors,
                                          'form': formset,
                                          'reports': Report.objects.all()},
                                          context_instance=RequestContext(request))
    else:
        return render_to_response('reports/reports.html',{
                                  'form': formset,
                                  'reports': Report.objects.all()},
                                  context_instance=RequestContext(request))

@login_required
@requires_csrf_token
def search(request):
    query_string = ''
    found_entries = None
    #q from button in html
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        #currently manually need to input the model fields to search through
        entry_query = get_query(query_string,[
                                'crime_date',
                                'resolve_days',
                                'jail_time',
                                'num_involved',
                                'creature',
                                'location',
                                'trial_location',
                                'violation_description',
                                'mpa',
                                'fine',
                                'update_date'])
        found_entries = Report.objects.filter(entry_query).order_by('crime_date')

    return render_to_response('reports/results.html',{
                              'query_string': query_string,
                              'found_entries': found_entries },
                              context_instance=RequestContext(request))

@login_required
def date_filter(request):
    start_date = ''
    end_date = ''
    found_entries = None
    if('start_date' in request.GET):
        start_date = request.GET['start_date']
    if('end_date' in request.GET):
        end_date = request.GET['end_date']
    found_entires = Report.objects.filter(crime_date__range=[start_date,end_date]).order_by('crime_date')
    return render_to_response('reports/results.html',{
                              'found_entries': found_entires },
                              context_instance=RequestContext(request))

@login_required
def rank(request,rank_by,reverse):
    if(reverse == 'true'):
        rank_by = '-'+rank_by
        result = Report.objects.all().order_by(rank_by)
    else:
        result = Report.objects.all().order_by(rank_by)

    return render_to_response('reports/reports.html',{
                              'reports': result },
                              context_instance=RequestContext(request))

@login_required
def detail(request,report_id):
    return render_to_response('reports/detail.html',{
                              'report': Report.objects.get(pk=report_id) },
                              context_instance=RequestContext(request))

@login_required
def delete_report(request,report_id):
    Report.objects.get(pk=report_id).delete()
    return render_to_response('reports/reports.html',{
                              'reports': Report.objects.all() },
                              context_instance=RequestContext(request))
