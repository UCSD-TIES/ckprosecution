import os
from django.contrib.auth.decorators import login_required
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
def create_report(request):
	form = ReportForm(request.POST or None)
	if form.is_valid():
		#report = form.save()
		report.save()
	return render_to_response('##')

@login_required
def update_report(request, report_id):
	report = get_object_or_404(Report, pk=report_id)
	form = ReportForm(request.POST or None, instance=report)
	if form.is_valid():
		report=form.save()
		report.save()
	return render_to_response('##')

@login_required
def delete_report(request, report_id):
	delete = Report.objects.get(pk=report_id).delete()

	return render_to_response('##')

@login_required
def compute_statistics(request):
	total_reports = Report.objects.all().count()
	
	# Start of Graphs
	
    ## Total Violations by Location ##
	location_stats_label = ""
	location_stats_data = []
	
	for location in Report.objects.all().distinct('location').values('location'):
		c_string = '' + str(location).lstrip("{'location': u'").rstrip("'}")
		percentage = (float(Report.objects.filter(location=c_string).count()) / total_reports) * 100
		location_stats_label+= str(c_string) + " " + str(round(percentage, 2)) + "%|"
		location_stats_data.append(percentage)
    
	location_graph = Pie(location_stats_data)
	location_graph.title('Total Violations by Location')
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
        'location_graph': location_graph,
        'creature_graph': creature_graph
        },
        context_instance=RequestContext(request)
    )

from reports.forms import ReportForm

@login_required
def view_reports(request):
	formset = ReportForm()
	if request.method == 'POST':
		form = ReportForm(request.POST)
		if form.is_valid():
			new_report= form.save()
			return render_to_response('reports/reports.html',{"success": "success","form": formset,"reports": Report.objects.all(),},
				context_instance=RequestContext(request))
		else:
			return render_to_response('reports/reports.html',{"error": form.errors,"form": formset, "reports": Report.objects.all(),},
				context_instance=RequestContext(request))
	else:
		return render_to_response('reports/reports.html',{"form": formset, "reports": Report.objects.all(),},
							context_instance=RequestContext(request))
@login_required
@requires_csrf_token
def search(request):
	print 'hello'
	query_string = ''
	found_entries = None
	if ('q' in request.GET) and request.GET['q'].strip():
		print 'hello WORLD'
		query_string = request.GET['q']
		print 'hello'
		#currently manually need to input the model fields to search through
		entry_query = get_query(query_string, ['crime_date', 'resolve_days','jail_time','num_involved','creature',
								'location','trial_location','violation_description', 'mpa','fine','update_date'])
		found_entries = Report.objects.filter(entry_query).order_by('location')

	return render_to_response('search/search.html',{ 'query_string': query_string, 'found_entries': found_entries },
							context_instance=RequestContext(request))
	
	
