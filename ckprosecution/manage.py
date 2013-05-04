#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ckprosecution.settings")

	from django.core.management import execute_from_command_line
	
	if(sys.argv[1] == "fake"):
		from reports.models import *
		for x in xrange(1, 11):
			a = x
			p = Report(
					crime_date = '1991-01-01',
					resolve_days = a,
					jail_time = 1,
					num_involved = a,
					creature = 'whale',
					location = 'san diego',
					trial_location = 'san diego',
					violation_description = 'blah;',
					mpa = 'blah',
					fine = a,
					update_date = '2005-12-12')
			p.save()
		
	else:
		execute_from_command_line(sys.argv)