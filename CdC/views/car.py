from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.http import JsonResponse
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

from equipamentos.settings import BASE_DIR
ajax_template = {
            "cars_free":BASE_DIR+"/CdC/templates/car/cars_free_table_template.html",
            "cars_inuse":BASE_DIR+"/CdC/templates/car/cars_inuse_table_template.html"
        }  

class Cars(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_move'

    def get(self, request, *args, **Kwargs):
         
        cars = Car.objects.all().filter(in_use=False)
        context ={
            "where":"cars",
            "cars":cars,
            "places":Place.objects.all()
        }
        return render(request, 'car/carros.html', context)
    
    def post(self, request, *args, **kwargs):
        self.dinamic_templates = {
            "requestTemplate":self.get_template,
            "get_car":self.set_car_inuse,
            "set_car":self.set_car_indestiny
        }
        json_request = json.loads(request.body)
        data = self.dinamic_templates[json_request["type"]](request,json_request)
        return JsonResponse(data)


    def get_template(self, request, dict, *args, **kwargs):
        if(dict["args"][0]=="cars_free"):
            cars = Car.objects.all().filter(in_use=False)
        else:
            cars = Car.objects.all().filter(in_use=True)
        context =Context({"cars":cars,
                          "places":Place.objects.all(),
                          "can_see_log":request.user.has_perm('CdC.can_see_log') })
        template = open(ajax_template[dict["args"][0]],'r').read()
        html = Template(template).render(context)
        data = {
            "type":dict["type"],
            "args":dict["args"],
            "payloadHTML":html
        }
        return data


    def set_car_inuse(self, request, dict, *args, **kwargs):
        try:
            car = Car.objects.get(licensePlate=dict["args"][0].lower())
            previous_position = car.where
            car.in_use = True
            car.responsible = request.user
            car.where = None
            car.update(origin=previous_position, user=request.user, typeLog=1)
        except:
            data = {
                    "type":dict["type"],
                    "args":dict["args"],
                    "status":"fail" }
            return data
        data = {  "type":dict["type"],
                  "args":dict["args"],
                  "status":"success" }
        return data

    def set_car_indestiny(self, request, dict, *args, **kwargs):
        try:
            car = Car.objects.get(licensePlate=dict["args"][1].lower())
            car_last_log = (Carlog.objects.all().filter(licensePlate=dict["args"][1].lower())).order_by("-date")[0]
            car.where = Place.objects.get(name=dict["args"][0])
            car.in_use = False
            car.update(origin=None, user=request.user, typeLog=2)
        except:
            data = {
                    "type":dict["type"],
                    "args":dict["args"],
                    "status":"fail"
            }
            return data
        data = {  "type":dict["type"],
                  "args":dict["args"],
                  "status":"success" }
        return data

class CarAdd(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_manager_equipment'
#--------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        self.functions={
            "createCar":self.create_car
        }
        super(CarAdd, self).__init__()
#--------------------------------------------------------------------------------
    def get(self, request, *args, **Kwargs):
        context={
                "places":Place.objects.all(),
                }
        return render(request, 'Car/addcar.html', context)
#--------------------------------------------------------------------------------
    def post(self, request, *args, **kwargs):
        json_request=json.loads(request.body)
        data = self.functions[json_request["type"]](request, json_request)
        return JsonResponse(data)
#--------------------------------------------------------------------------------
    def create_car(self, request, json_request, *args, **kwargs):
        try:
           json_payload=json_request["payload"]
           newCar=Car(
               licensePlate=json_payload["license"],
               name=json_payload["name"],
               where=Place.objects.get(name=json_payload["place"]),
               is_active=json_payload["isactive"],
               in_use=False
           )
           newCar.create(user=request.user)
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
class CarEdit(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_manager_equipment'
#--------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        self.functions={
            "search":self.get_car_by_license,
            "editcar":self.edit_car,
            "deletecar":self.delete_car_by_license
        }
        super(CarEdit, self).__init__(*args, **kwargs)
#--------------------------------------------------------------------------------
    def get(self, request, *args, **kwargs):
        context={
                "places":Place.objects.all(),
                }
        return render(request, 'Car/editcar.html', context)
#--------------------------------------------------------------------------------
    def post(self, request, *args, **kwargs):
        json_request=json.loads(request.body)
        data = self.functions[json_request["type"]](request, json_request)
        return JsonResponse(data)
#--------------------------------------------------------------------------------
    def get_car_by_license(self, request, json_request, *args, **kwargs):
        
        json_payload=json_request["payload"]
        fields=serializers.serialize('json', 
            Car.objects.all().filter(licensePlate=json_payload["license"].lower()),
            fields=('name', "is_active"))
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
    def edit_car(self, request, json_request, *args, **kwargs):
        try:
           json_payload=json_request["payload"]
           getCar=Car.objects.get(licensePlate=json_payload["license"].lower())
           getCar.name=json_payload["name"]
           getCar.is_active=json_payload["isactive"]
           getCar.edit(user=request.user)
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
    def delete_car_by_license(self, request, json_request, *args, **kwargs):
        try:
            Car.objects.get(licensePlate=json_request["payload"]["license"].lower()).log_and_delete(user=request.user)
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