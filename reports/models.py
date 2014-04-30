from django.db import models

# Reports Model
# TODO: Field to hold links to relevant news articles (possible cached version?)
class Report(models.Model):
    crime_date = models.DateField(blank = True, null = True)
    resolve_days = models.IntegerField(blank = True, max_length=11)
    num_involved = models.IntegerField(blank = True, max_length=11)
    creature = models.CharField(blank = True, max_length=45)
    mpalocation = models.CharField(blank = True, max_length=45)
    location = models.CharField(blank = True, max_length=45)
    trial_location = models.CharField(blank = True, max_length=45) #city where crime was tried
    violation_description = models.CharField(blank = True, max_length=500)
    fine = models.DecimalField(max_digits=11, decimal_places=2, blank = True, max_length=11)
    update_date = models.DateField(auto_now=True)
    jail_time = models.BooleanField(default = False)
    mpa = models.BooleanField(default = False)

    def get_absolute_url(self):
        return "/reports/report_%i" % self.id
