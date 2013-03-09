from django.db import models

# Create your models here.
class Report(models.Model):
	crime_date = models.DateField(blank = True, null = True)
	resolve_days = models.IntegerField(blank = True, max_length=11)
	jail_time = models.BooleanField(default = False)
	num_involved = models.IntegerField(blank = True, max_length=11)
	creature = models.CharField(blank = True, max_length=45)
	location = models.CharField(blank = True, max_length=45)
	trial_location = models.CharField(blank = True, max_length=45) #city where crime was tried
	violation_description = models.CharField(blank = True, max_length=100)
	mpa = models.BooleanField(default = False)
	fine = models.IntegerField(blank = True, default = False, max_length=11)
	#not sure how to add variable amounts of links to articles to a model
	update_date = models.DateField(blank = True, null = True)
	
	
	
	