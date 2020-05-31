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
    is_active = models.BooleanField()

    def __str__(self):
        return self.licensePlate + " " + self.name
    
    def update(self,*args,**kwargs):
        Carlog(licensePlate=str(self.licensePlate).lower(),
         origin=kwargs.pop("origin"),
          destiny=self.where,
           responsible=kwargs.pop("user"),
           type_of_log=kwargs.pop("typeLog")).save()
        self.save(*args,**kwargs)
    
    def create(self, *args, **kwargs):
        Carlog(licensePlate=str(self.licensePlate).lower(),
         origin=self.where, destiny=self.where,
          responsible=kwargs.pop("user"),
            type_of_log=7).save()
        self.save(*args, **kwargs)

    def log_and_delete(self, *args, **kwargs):
        Carlog(licensePlate=str(self.licensePlate).lower(),
         origin=self.where, destiny=self.where,
          responsible=kwargs.pop("user"),
            type_of_log=6).save()
        self.delete(*args, **kwargs)
    
    def edit(self, *args, **kwargs):
        Carlog(licensePlate=str(self.licensePlate).lower(),
         origin=self.where, destiny=self.where,
          responsible=kwargs.pop("user"),
            type_of_log=8).save()
        self.save(*args, **kwargs)