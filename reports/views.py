import os
from django.utils import simplejson
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime

from reports.models import Report
from reports.forms import ReportForm

from GChartWrapper import *


def create_report(request):
	form = ReportForm(request.POST or None)
	if form.is_valid():
		report = form.save()
		report.save()
	return render_to_response('##')

def update_report(request, report_id):
	report = get_object_or_404(Report, pk=report_id)
	form = ReportForm(request.POST or None, instance=report)
	if form.is_valid():
		report=form.save()
		report.save()
	return render_to_response('##')

def delete_report(request, report_id):
	delete = Report.objects.get(pk=report_id).delete()

	return render_to_response('##')

def compute_statistics(request):
	total_reports = Report.objects.all().count()
	location_stats = []
	
	for location in Report.objects.all().distinct('location').values('location'):
		percentage = (Report.objects.filter(location=location).count() / total_reports) * 100
		location_stats.append((location, percentage))

	##Type of Creatures affected by All Violations ##
	creature_stats_label = ""
	creature_stats_data = []
	
	for creature in Report.objects.all().distinct('creature').values('creature'):
		c_string = '' + str(creature).lstrip("{'creature': u'").rstrip("'}")
		percentage = (float(Report.objects.filter(creature=c_string).count()) / total_reports) * 100
		creature_stats_label+= str(c_string) + " " + str(round(percentage, 2)) + "%|"
		creature_stats_data.append(percentage)
		
	creature_graph = Pie(creature_stats_data)
	creature_graph.title('Type of Creatures Affected by All Violations')
	creature_graph.size(600,300)
	creature_graph.label(creature_stats_label.rstrip("|"))
	creature_graph.color('0000aa')
		
	#End of graphs
		
	return render_to_response('reports/statistics.html', {
        'location_stats': location_stats,
        'creature_graph': creature_graph
        },
        context_instance=RequestContext(request)
    )
	
	

		

	
