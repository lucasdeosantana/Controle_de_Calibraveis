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

class EquipmentView(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_move'
    def get(self, request, equipPlace, *args, **Kwargs):
        where = Place.objects.get(name=equipPlace)
        equipmentList = (Equipment.objects.all().filter(where=where, in_calibration=0)).order_by('date_validity')
        context={
                "places":Place.objects.all(),
                "equipments":equipmentList,
                "where":equipPlace
                }
        return render(request, 'equipment.html', context)