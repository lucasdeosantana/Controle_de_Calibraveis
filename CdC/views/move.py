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

class MoveView(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_move'
    def get(self, request, *args, **Kwargs):
        context={"where":"move",
                 "places":Place.objects.all()
                                }
        return render(request,'equipment/move.html', context)

    def post(self, request, *args, **Kwargs):
        self.functs={
            "doMove":self.do_move,
            "request":self.get_equipment
        }
        json_request = json.loads(request.body)
        answer = self.functs[json_request["type"]](json_request, request)
        return JsonResponse(answer)
    def get_equipment(self,data, *args, **kwargs):
        if(data["equipmentCode"].isnumeric()):
            equipment = Equipment.objects.get(code=data["equipmentCode"])
            if(equipment.in_calibration!=0):
                data = {"type":"Warning"}
            else:
                data = {
                        "type":"EquipmentInformation",
                        "name":equipment.name,
                        "in_station":equipment.where.name
                }
        else:
            car = Car.objects.get(placa=data["equipmentCode"])
            data = {
                        "type":"EquipmentInformation",
                        "name":car.name,
                        "in_station":car.where
                }
        return data
        
    def do_move(self, data, request, *args, **kwargs):
        if(data["equipmentCode"].isnumeric()):
            equipment = Equipment.objects.get(code=int(data["equipmentCode"]))
            if(data["for"]== "Calibration"):
                equipment.in_calibration = 1
                type_log = 2
                equipment.where = Place.objects.get(name="Base")
            else:
                type_log = 1
                equipment.where = Place.objects.get(name=data["for"])
            equipment.move(origin = Place.objects.get(name=data["where"]), user = request.user, typeLog=type_log)
            data = {"type":"Success","equipmentCode": data["equipmentCode"]}
        return data
