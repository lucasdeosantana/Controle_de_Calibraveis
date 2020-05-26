from django.db import models
from .place import Place
from django.contrib.auth.models import User
class Log(models.Model):
    code = models.IntegerField()
    type_of_log=models.IntegerField()
    origin = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="OrigemLog")
    destiny = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="DestinoLog")
    date = models.DateTimeField(auto_now_add=True)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
class Carlog(models.Model):
    licensePlate = models.CharField(max_length=15, null=True)
    origin = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="Origem", null=True)
    destiny = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="Destino", null=True)
    date = models.DateTimeField(auto_now_add=True)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
