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
import os
from equipamentos.settings import BASE_DIR
ajax_template = {
            "cars_free":BASE_DIR+"/CdC/templates/cars_free_table_template.html",
            "cars_inuse":BASE_DIR+"/CdC/templates/cars_inuse_table_template.html"
        }  

class Cars(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_move'

    def get(self, request, *args, **Kwargs):
         
        cars = Car.objects.all().filter(in_use=None)
        context ={
            "where":"carros",
            "cars":cars,
            "places":places.objects.all()
        }
        return render(request, 'carros.html', context)
    
    def post(self, request, *args, **kwargs):
        print(BASE_DIR)
        self.dinamic_templates = {
            "requestTemplate":self.get_template,
            "get_car":self.set_car_inuse,
            "set_car":self.set_car_indestiny
        }
        json_request = json.loads(request.body)
        print(json_request)
        data = self.dinamic_templates[json_request["type"]](request,json_request)
        return JsonResponse(data)
    def get_template(self, request, dict, *args, **kwargs):
        if(dict["args"][0]=="cars_free"):
            cars = Car.objects.all().filter(in_use=None)
        else:
            cars = Car.objects.all().exclude(in_use=None)

        context =Context({"cars":cars,
                            "places":places.objects.all()
                                                            })
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
            car = Car.objects.get(placa=dict["args"][0])
            previous_position = car.position
            car.in_use = request.user.username
            car.position = "Em uso"
            car.save()
            create_log = carlog(placa=dict["args"][0], origem=previous_position, destino="Em Uso", responsible=request.user.username)
            create_log.save()
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
    def set_car_indestiny(self, request, dict, *args, **kwargs):
        try:
            car = Car.objects.get(placa=dict["args"][1])
            car_last_log = (carlog.objects.all().filter(placa=dict["args"][1])).order_by("-date")[0]
            car.position = dict["args"][0]
            car.in_use = None
            car_create_log = carlog(placa=dict["args"][1], origem=car_last_log.origem, destino=dict["args"][0], responsible=request.user.username)
            car_create_log.save()
            car.save()
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