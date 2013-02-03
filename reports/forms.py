from django.forms import Modelform
from reports.models import Report

class ReportForm(Modelform):
	class Meta:
		model = Report