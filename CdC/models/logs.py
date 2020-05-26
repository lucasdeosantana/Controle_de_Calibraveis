from django.db import models

class Log(models.Model):
    code = models.IntegerField()
    type_of_log=models.IntegerField()
    origin = models.CharField(max_length=30,blank=False,null=False)
    destiny = models.CharField(max_length=30, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    responsible = models.CharField(max_length=10, blank=False, null=False)
    observation = models.CharField(max_length=100, blank=True, null=True)

class Carlog(models.Model):
    licensePlate = models.CharField(max_length=30, blank=True,null=True)
    origin = models.CharField(max_length=30,blank=False,null=False)
    destiny = models.CharField(max_length=30, blank=True, null=False)
    date = models.DateTimeField(auto_now_add=True)
    responsible = models.CharField(max_length=10, blank=False, null=False)