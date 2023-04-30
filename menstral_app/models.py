from django.db import models


# Create your models here.

class Cycle(models.Model):
    day = models.CharField(max_length=2, blank=False)
    date = models.DateField(blank=False)
    ovulation_date = models.DateField(null=True)
    flow_dates = models.DateField(null=True)
    fertile_dates = models.DateField(null=True)
    safe_periods = models.DateField(null=True)

# class ImportantDays(models.Model):
#     ovulation_date = models.DateField()
#     flow_dates = models.DateField()
#     fertile_dates = models.DateField()
#     safe_periods = models.DateField()
