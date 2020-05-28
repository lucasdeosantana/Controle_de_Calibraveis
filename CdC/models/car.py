from django.db import models
from .place import Place
from .logs import Carlog
from django.contrib.auth.models import User

class Car(models.Model):
    licensePlate = models.CharField('Placa',max_length=8, blank=False, null=False, unique=True)
    name = models.CharField('Modelo',max_length=100, blank=False, null=False)
    where = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    in_use =models.BooleanField(null=True)

    def __str__(self):
        return self.licensePlate + " " + self.name
    
    def update(self,*args,**kwargs):
        Carlog(licensePlate=str(self.licensePlate).lower(), origin=kwargs.pop("origin"), destiny=self.where, responsible=kwargs.pop("user")).save()
        self.save(*args,**kwargs)