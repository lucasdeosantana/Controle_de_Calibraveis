from django.db import models
from datetime import datetime, timedelta
from .place import Place
from .logs import Log
from dateutil.relativedelta import relativedelta


class Equipment(models.Model):
    code = models.IntegerField('Codigo do Equipamento',null=False,blank=False, unique=True)
    name = models.CharField('Nome', max_length=244, null=False, blank=False)
    nickName = models.CharField('Apelido', max_length=100, blank=True, null=True)
    where = models.OneToOneField(Place, on_delete=models.CASCADE, null=True)
    date_calibration = models.DateField('Data de Calibração', blank=False, null=False)
    validity_time=models.IntegerField("Meses de validade", blank=True, null=True)
    date_validity=models.DateField('Data de validade se preenche automatico se deixado em branco',blank=True, null=True)
    in_calibration=models.IntegerField()

    def __str__(self):
        return str(self.code) + " " + self.name

    def save(self, *args, **kwargs):
        if not self.date_validity:
            self.date_validity = self.date_calibration + relativedelta(months=self.validity_time)
        super(Equipment, self).save(*args, **kwargs)
    def save_special(self, *args, **kwargs):
        Log(code=self.code, origin=kwargs.pop("origin"), destiny=self.where,
             type_of_log=kwargs.pop("typeLog"),
              responsible=kwargs.pop("user")).save()
        self.date_validity = self.date_calibration + relativedelta(months=self.validity_time)
        self.save(args, kwargs)
    def move(self, *args,**kwargs):
        Log(code=self.code, origin=kwargs.pop("origin"), destiny=self.where,
             type_of_log=kwargs.pop("typeLog"),
              responsible=kwargs.pop("user")).save()
        self.save(args, kwargs)
        
