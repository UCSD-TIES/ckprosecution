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
	delete = Reports.objects.get(pk=report_id).delete()

	return render_to_response('##')