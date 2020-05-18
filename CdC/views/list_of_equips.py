from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import Context, Template
from django.utils.timezone import datetime
from django.utils.dateparse import parse_date
import json
from CdC.models import *
class list_of_equips(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_move'
    def get(self, request, station, *args, **Kwargs):
<<<<<<< HEAD
        self.urlshort ={
            "PVS":"Patio",
            "MBI":"Morumbi",
            "BUT":"Butantã",
            "PIN":"Pinheiros",
            "FAL":"Faria Lima",
            "FRA":"Fradique Coutinho",
            "FRE":"Oscar Freire",
            "PTA":"Paulista",
            "HIG":"Higienopolis",
            "REP":"Republica",
            "LUZ":"Luz",
            "BASE":"Base"
            }
        equipmentList = (Equipament.objects.all().filter(position=self.urlshort[station])).order_by('date_validity')
        print(equipmentList)
        context={
                "equipments":equipmentList,
                "where":self.urlshort[station]
=======
        where = places.objects.get(viewName=station)
        equipmentList = (Equipament.objects.all().filter(position=where.name)).order_by('date_validity')
        print(equipmentList)
        context={
                "places":places.objects.all(),
                "equipments":equipmentList,
                "where":station
>>>>>>> Uso_Geral
                }
        return render(request, 'equipment.html', context)