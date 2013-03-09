import os
from django.utils import simplejson
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime

#This import model is incorrect but I don't think the model should be plural
from reports.models import Report
from reports.forms import ReportForm


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
	creature_stats = []
	for location in Report.objects.all().values(location).distinct():
		percentage = (Report.objects.filter(location=location).count() / total_reports) * 100
		location_stats.append((location, percentage))

	for creature in Report.objects.all().values(creature).distinct():
		percentage = (Report.objects.filter(creature=creature).count() / total_reports) * 100
		creature_stats.append((creature, percentage))

	return render_to_response('reports/statistics.html', {
        'location_stats': location_states,
        'creature_stats': creature_stats
        },
        context_instance=RequestContext(request)
    )
	
	

		

	
