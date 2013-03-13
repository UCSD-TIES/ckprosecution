# Create your views here.
import os
from django.utils import simplejson
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.context_processors import csrf
from django.views.decorators.csrf import requires_csrf_token

def landing(request):
		
	return render_to_response('base.html', {
        },
        context_instance=RequestContext(request)
    )