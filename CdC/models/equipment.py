from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Equipament(models.Model):
    codigo = models.IntegerField('Codigo do Equipamento',null=False,blank=False, unique=True)
    nome = models.CharField('Nome', max_length=244, null=False, blank=False)
    apelido = models.CharField('Apelido', max_length=100, blank=True, null=True)
    position = models.CharField('Localização', max_length=30, blank=True, null=True, )
    date_calibration = models.DateField('Data de Calibração', blank=False, null=False)
    validity_time=models.IntegerField("Meses de validade", blank=True, null=True)
    date_validity=models.DateField('Data de validade se preenche automatico se deixado em branco',blank=True, null=True)
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