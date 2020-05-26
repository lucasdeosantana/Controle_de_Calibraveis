from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    viewName=models.CharField(max_length=30, blank=False, null=False)