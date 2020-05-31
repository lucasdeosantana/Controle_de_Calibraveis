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
from django.core import serializers

class EquipmentView(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_move'
#--------------------------------------------------------------------------------
    def get(self, request, equipPlace, *args, **Kwargs):
        where = Place.objects.get(name=equipPlace)
        equipmentList = (Equipment.objects.all().filter(where=where, in_calibration=0, is_active=True)).order_by('date_validity')
        context={
                "places":Place.objects.all(),
                "equipments":equipmentList,
                "where":equipPlace
                }
        return render(request, 'equipment/equipment.html', context)
#_______________________________________________________________________________
class EquipmentAdd(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_manager_equipment'
#--------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        self.functions={
            "createEquipment":self.create_equipment
        }
        super(EquipmentAdd, self).__init__()
#--------------------------------------------------------------------------------
    def get(self, request, *args, **Kwargs):
        context={
                "places":Place.objects.all(),
                }
        return render(request, 'equipment/addequipment.html', context)
#--------------------------------------------------------------------------------
    def post(self, request, *args, **kwargs):
        json_request=json.loads(request.body)
        data = self.functions[json_request["type"]](request, json_request)
        return JsonResponse(data)
#--------------------------------------------------------------------------------
    def create_equipment(self, request, json_request, *args, **kwargs):
        try:
           json_payload=json_request["payload"]
           newEquipment=Equipment(
               code=json_payload["code"],
               name=json_payload["name"],
               where=Place.objects.get(name="Base"),
               date_calibration=datetime.strptime(json_payload["calibrationdata"], "%Y-%m-%d").date(),
               validity_time=int(json_payload["months"]),
               in_calibration=0,
               is_active=json_payload["isactive"]
           )
           if(json_payload["validitydata"]!=""):
               newEquipment.date_validity=datetime.strptime(json_payload["validitydata"], "%Y-%m-%d").date()
           newEquipment.create(user=request.user)
           data={
               "type":json_request["type"],
               "status":"success"
           }
        except:
            data={
                "type":json_request["type"],
                "status":"fail"
            }
        return data
#_______________________________________________________________________________
class EquipmentEdit(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_manager_equipment'
#--------------------------------------------------------------------------------
    def __init__(self):
        self.functions={
            "search":self.get_equip_by_code,
            "editequip":self.edit_equipment,
            "deleteequip":self.delete_equipment_by_code
        }
        super(EquipmentEdit, self).__init__()
#--------------------------------------------------------------------------------
    def get(self, request, *args, **kwargs):
        context={
                "places":Place.objects.all(),
                }
        return render(request, 'equipment/editequipment.html', context)
#--------------------------------------------------------------------------------
    def post(self, request, *args, **kwargs):
        json_request=json.loads(request.body)
        data = self.functions[json_request["type"]](request, json_request)
        return JsonResponse(data)
#--------------------------------------------------------------------------------
    def get_equip_by_code(self, request, json_request, *args, **kwargs):
        json_payload=json_request["payload"]
        fields=serializers.serialize('json', 
            Equipment.objects.all().filter(code=json_payload["code"]),
            fields=('name', 'date_calibration', "validity_time", "date_validity", "is_active"))
        if(fields!="[]"):
            data = {
                "type":json_request["type"],
                "payload":fields,
                "status":"success"
            }
        else:
            data = {
                "type":json_request["type"],
                "status":"fail"
            }
        return data
#---------------------------------------------------------------------------------3
    def edit_equipment(self, request, json_request, *args, **kwargs):
        try:
            json_payload=json_request["payload"]
            getEquipment=Equipment.objects.get(code=int(json_payload["code"]))
            getEquipment.name=json_payload["name"]
            getEquipment.date_calibration=datetime.strptime(json_payload["calibrationdata"], "%Y-%m-%d").date()
            getEquipment.validity_time=int(json_payload["months"])
            getEquipment.is_active=json_payload["isactive"]
            if(json_payload["validitydata"]!=""):
               getEquipment.date_validity=datetime.strptime(json_payload["validitydata"], "%Y-%m-%d").date()
            else:
               getEquipment.date_validity=None 
            getEquipment.edit(user=request.user)
            data = {
                "type":json_request["type"],
                "status":"success"
            }
        except:
            data = {
                "type":json_request["type"],
                "status":"fail"
            }
        return data
#-----------------------------------------------------------------------------------
    def delete_equipment_by_code(self, request, json_request, *args, **kwargs):
        try:
            Equipment.objects.get(code=json_request["payload"]["code"]).log_and_delete(user=request.user)
            data = {
                "type":json_request["type"],
                "status":"success"
            }
        except:
            data = {
                "type":json_request["type"],
                "status":"fail"
            }
        return data