from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Log(models.Model):
    codigo = models.IntegerField()
    type_of_log=models.IntegerField()
    origem = models.CharField(max_length=30,blank=False,null=False)
    destino = models.CharField(max_length=30, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    responsible = models.CharField(max_length=10, blank=False, null=False)
    observation = models.CharField(max_length=100, blank=True, null=True)

class Carlog(models.Model):
    placa = models.CharField(max_length=30, blank=True,null=True)
    origem = models.CharField(max_length=30,blank=False,null=False)
    destino = models.CharField(max_length=30, blank=True, null=False)
    date = models.DateTimeField(auto_now_add=True)
    responsible = models.CharField(max_length=10, blank=False, null=False)