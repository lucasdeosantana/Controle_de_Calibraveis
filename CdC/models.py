from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

stations = (
    ("Patio","Patio"),
    ("Morumbi","Morumbi"),
    ("Butantã","Butantã"),
    ("Pinheiros","Pinheiros"),
    ("Faria Lima","Faria Lima"),
    ("Fradique Coutinho","Fradique Coutinho"),
    ("Oscar Freire","Oscar Freire"),
    ("Paulista","Paulista"),
    ("Higienopolis","Higienopolis"),
    ("Republica","Republica"),
    ("Luz","Luz"),
    ("Calibração","Calibração"),
    ("Base","Base")
)
stationscar = (
    ("Patio","Patio"),
    ("Morumbi","Morumbi"),
    ("Butantã","Butantã"),
    ("Pinheiros","Pinheiros"),
    ("Faria Lima","Faria Lima"),
    ("Fradique Coutinho","Fradique Coutinho"),
    ("Oscar Freire","Oscar Freire"),
    ("Paulista","Paulista"),
    ("Higienopolis","Higienopolis"),
    ("Republica","Republica"),
    ("Luz","Luz"),
    ("Calibração","Calibração"),
    ("Em uso","Em uso")
)
# Create your models here.
class log(models.Model):
    codigo = models.IntegerField()
    origem = models.CharField(max_length=30,blank=False,null=False,choices=stations)
    destino = models.CharField(max_length=30, blank=False, null=False,choices=stations)
    date = models.DateTimeField(auto_now=True)
    responsible = models.CharField(max_length=10, blank=False, null=False)
    observation = models.CharField(max_length=100, blank=True, null=True)
    type_of_log = models.IntegerField(null=True)

class carlog(models.Model):
    placa = models.CharField(max_length=30, blank=True,null=True)
    origem = models.CharField(max_length=30,blank=False,null=False,choices=stationscar)
    destino = models.CharField(max_length=30, blank=False, null=False,choices=stationscar)
    date = models.DateTimeField(auto_now=True)
    responsible = models.CharField(max_length=10, blank=False, null=False)

class Equipament(models.Model):
    codigo = models.IntegerField('Codigo do Equipamento',null=False,blank=False, unique=True)
    nome = models.CharField('Nome', max_length=244, null=False, blank=False)
    apelido = models.CharField('Apelido', max_length=100, blank=True, null=True)
    position = models.CharField('Localização', max_length=30, blank=True, null=True,choices=stations)
    date_calibration = models.DateField('Data de Calibração', blank=False, null=False)
    date_validity=models.DateField('Data de validade, se prenche com 1 ano se não informado',blank=True, null=True)
    in_calibration=models.IntegerField()

    def __str__(self):
        return str(self.codigo) + " " + self.nome

    def save(self, *args, **kwargs):
        if(self.date_validity == None):
            self.date_validity = self.date_calibration+timedelta(days=365)
        super(Equipament, self).save(*args, **kwargs)
    def save_special(self):
        self.date_validity = self.date_calibration+timedelta(days=365)
        self.save()
    class Meta:
        permissions=[ 
            ('can_move','Pode mover equipamentos'),
            ('can_receive', 'Pode receber equipamentos de calibração'),
            ('can_see_log', 'Pode ver os logs')
        ]
class Car(models.Model):
    placa = models.CharField('Placa',max_length=8, blank=False, null=False, unique=True)
    nome = models.CharField('Modelo',max_length=100, blank=False, null=False)
    position = models.CharField('Localização',max_length=30, null=True, blank=True,choices=stationscar)
    in_use =models.CharField('Utilizador', max_length=15, blank=True, null=True)

    def __str__(self):
        return self.placa + " " + self.nome
