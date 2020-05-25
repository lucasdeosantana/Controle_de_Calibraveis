from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Place(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    viewName=models.CharField(max_length=30, blank=False, null=False)