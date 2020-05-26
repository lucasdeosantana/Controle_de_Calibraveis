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
        where = places.objects.get(viewName=station)
        equipmentList = (Equipment.objects.all().filter(where=where.name)).order_by('date_validity')
        context={
                "places":places.objects.all(),
                "equipments":equipmentList,
                "where":station
                }
        return render(request, 'equipment.html', context)