from django.db import models

class Car(models.Model):
    licensePlate = models.CharField('Placa',max_length=8, blank=False, null=False, unique=True)
    name = models.CharField('Modelo',max_length=100, blank=False, null=False)
    where = models.CharField('Localização',max_length=30, null=True, blank=True)
    in_use =models.CharField('Utilizador', max_length=15, blank=True, null=True)

    def __str__(self):
        return self.licensePlate + " " + self.name