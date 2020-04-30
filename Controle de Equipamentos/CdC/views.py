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
import json
from .models import *

base = "Faria Lima"

class move(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_move'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(move, self).dispatch(request, *args, **kwargs)
    def get(self, request, *args, **Kwargs):
        return render(request,'move.html')

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
            equipment = Equipament.objects.get(codigo=data["equipmentCode"])
            if(equipment.in_calibration!=0):
                data = {"type":"Warning"}
            else:
                data = {
                        "type":"EquipmentInformation",
                        "name":equipment.nome,
                        "in_station":equipment.position
                }
        else:
            car = Car.objects.get(placa=data["equipmentCode"])
            data = {
                        "type":"EquipmentInformation",
                        "name":car.nome,
                        "in_station":car.position
                }
        return data
    def do_move(self, data, request, *args, **kwargs):
        if(data["equipmentCode"].isnumeric()):
            equipment = Equipament.objects.get(codigo=data["equipmentCode"])
            if(data["for"]== "Calibração"):
                equipment.in_calibration = 1
                equipment.position = base
            else:
                equipment.position = data["for"]
            create_log = log(codigo = data["equipmentCode"], origem = data["where"], destino = data["for"], responsible = request.user.username)
            create_log.save()
            equipment.log.add(create_log)
            equipment.save()
            data = {"type":"Success","equipmentCode": data["equipmentCode"]}
        else:
            car = Car.objects.get(placa=data["equipmentCode"])
            logcar = carlog(placa=data["equipmentCode"], origem = data["where"], destino = data["for"], responsible = request.user.username)
            logcar.save()
            car.position = data["for"]
            car.log.add(logcar)
            car.save()
            data = {"type":"Success","equipmentCode": data["equipmentCode"] }
        return data

def do_login(request, *args, **kwargs):
    if request.method == 'POST':
        user = authenticate(username=request.POST['user'], password=request.POST['pass'])
        if user is not None:
            login(request, user)
            return redirect("/move")
    return render(request, 'login.html')

def do_logout(request, *args, **kwargs):
    logout(request)
    return redirect("/login/")

class list_of_equips(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_move'
    def get(self, request, station, *args, **Kwargs):
        self.urlshort ={
            "PVS":"Patio",
            "MBI":"Morumbi",
            "BUT":"Butantã",
            "PIN":"Pinheiros",
            "FAL":"Faria Lima",
            "FRA":"Fradique Coutinho",
            "FRE":"Oscar Freire",
            "PTA":"Paulista",
            "HIG":"Higeanopolis",
            "REP":"Republica",
            "LUZ":"Luz",
            }
        equipmentList = (Equipament.objects.all().filter(position=self.urlshort[station])).order_by('date_validity')
        print(equipmentList)
        context={
                "equipments":equipmentList,
                "where":self.urlshort[station]
                }
        return render(request, 'equipment.html', context)

class superview(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_move'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(superview, self).dispatch(request, *args, **kwargs)

    def get(self, request, page, *args, **Kwargs):
        self.pages={
            "Calibration":"Calibration.html"
        }
        equips_for_calibration = (Equipament.objects.all().filter(in_calibration=1)).order_by('date_validity')
        context = {
            "equipments":equips_for_calibration
        }
        return render(request, self.pages[page], context)

    def post(self, request, *args, **kwargs):
        self.functs ={
            "equipConfirm":self.get_Equipament_to_Confirm,
            "equipBack":self.get_Equipament_to_back,
            "confirm":self.confirm,
            "cancel":self.cancel,
            "return":self.return_to
        }
        json_request = json.loads(request.body)
        table= self.functs[json_request["type"]]()
        print(table)
        data ={
                "type":json_request["type"],
                "table":table
        }
        return JsonResponse(data)
    
    def get_Equipament_to_Confirm(self):
        equips_for_calibration = (Equipament.objects.all().filter(in_calibration=1)).order_by('date_validity')
        template = Template("""
            {% for equipment in equipments %}
            <tr class="bg" id="{{ equipment.codigo }}">
                <th scope="row">{{ equipment.codigo }}</th>
                <td>{{ equipment.date_validity|date:"F/Y" }}</td>
                <td>{{ equipment.nome }}</td>
                <td><button class="btn btn-primary" onclick="button_received({{ equipment.codigo }}, 'confirm')"><i class="fa fa-check"></i></button><button
                    class="btn btn-danger" onclick="button_received({{ equipment.codigo }}, 'cancel')"><i class="fa fa-times"></i></button></td>
            </tr>
            {% endfor %}""")
        context = Context({"equipments":equips_for_calibration})
        #print(template.render(context))
        return template.render(context)
    
    def get_Equipament_to_back(self):
        equips_for_calibration = (Equipament.objects.all().filter(in_calibration=2)).order_by('date_validity')
        template = Template("""
            {% if equipments %}
            {% for equipment in equipments %}
            <tr class="bg">
                <th scope="row">{{ equipment.codigo }}</th>
                <td><input type="date"></td>
                <td>{{ equipment.nome }}</td>
                <td><button class="btn btn-primary"><i class="fas fa-undo"></i></button></td>
            </tr>
            {% endfor %}
            {% else %}
            <tr class="bg">
                <th scope="row">NADA AQUI</th>
                <td>></td>
                <td></td>
                <td></td>
            </tr>
            {% endif %}
            """)
        context = Context({"equipments":equips_for_calibration})
        #print(template.render(context))
        return template.render(context) 	
        def confirm():
            pass
        def cancel():
            pass
        def return_to():
            pass