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
from .models import *

base = "Base"

ajax_template = {
    "cars_free":"Controle de Equipamentos/CdC/templates/cars_free_table_template.html",
    "cars_inuse":"Controle de Equipamentos/CdC/templates/cars_inuse_table_template.html"
}

class move(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_move'
    def get(self, request, *args, **Kwargs):
        context={"where":"move"}
        return render(request,'move.html', context)

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
            equipment.position = data["for"]
            create_log = log(codigo = data["equipmentCode"], origem = data["where"], destino = data["for"], responsible = request.user.username)
            create_log.save()
            equipment.save()
            data = {"type":"Success","equipmentCode": data["equipmentCode"]}
        else:
            car = Car.objects.get(placa=data["equipmentCode"])
            logcar = carlog(placa=data["equipmentCode"], origem = data["where"], destino = data["for"], responsible = request.user.username)
            logcar.save()
            car.position = data["for"]
            car.save()
            data = {"type":"Success","equipmentCode": data["equipmentCode"] }
        return data

def do_login(request, *args, **kwargs):
    print(request.body)
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
            "BASE":"Base"
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
    def get(self, request, page, *args, **Kwargs):
        self.pages={
            "Calibration":"Calibration.html"
        }
        equips_for_calibration = (Equipament.objects.all().filter(in_calibration=1)).order_by('date_validity')
        context = {
            "equipments":equips_for_calibration,
            "where":"Calibration"
        }
        return render(request, self.pages[page], context)

    def post(self, request, *args, **kwargs):
        self.functs ={
            "equipConfirm":self.get_Equipament_to_Confirm,
            "equipBack":self.get_Equipament_to_back,
            "to_confirm":self.to_confirm,
            "to_cancel":self.to_cancel,
            "to_return":self.to_return
        }
        json_request = json.loads(request.body)
        table= self.functs[json_request["type"]](json_request, Request=request)
        print(json_request)
        try:
            code = str(json_request["code"])
        except:
            code = None
        data ={
                "type":json_request["type"],
                "payload":table,
                "code":code,
        }
        return JsonResponse(data)
    
    def get_Equipament_to_Confirm(self, *args, **kwargs):
        equips_for_calibration = (Equipament.objects.all().filter(in_calibration=1)).order_by('date_validity')
        template = Template("""
            {% for equipment in equipments %}
            <tr class="bg" id="{{ equipment.codigo }}">
                <th scope="row">{{ equipment.codigo }}</th>
                <td>{{ equipment.date_validity|date:"F/Y" }}</td>
                <td>{{ equipment.nome }}</td>
                <td><button class="btn btn-primary" onclick="button_received({{ equipment.codigo }}, 'btn_confirm')"><i class="fa fa-check"></i></button><button
                    class="btn btn-danger" onclick="button_received({{ equipment.codigo }}, 'btn_cancel')"><i class="fa fa-times"></i></button></td>
            </tr>
            {% endfor %}""")
        context = Context({"equipments":equips_for_calibration})
        #print(template.render(context))
        return template.render(context)
    
    def get_Equipament_to_back(self, *args, **kwargs):
        equips_for_calibration = (Equipament.objects.all().filter(in_calibration=2)).order_by('date_validity')
        template = Template("""
            {% if equipments %}
            {% for equipment in equipments %}
            <tr class="bg" id="{{ equipment.codigo }}">
                <th scope="row">{{ equipment.codigo }}</th>
                <td><input type="date" id="d{{ equipment.codigo }}"></td>
                <td>{{ equipment.nome }}</td>
                <td><button class="btn btn-primary" onclick="button_received({{ equipment.codigo }}, 'btn_return')"><i class="fas fa-undo"></i></button></td>
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
    def to_confirm(self, dict, *args, **kwargs):
        try:
            equipment = Equipament.objects.get(codigo=dict["code"])
            equipment.in_calibration = 2
            equipment.save()
        except:
            return "Fail"
        create_log = log(codigo = dict["code"], origem = "Calibração", destino = "Calibração", responsible = kwargs["Request"].user.username)
        create_log.save()
        return "Success"
    def to_cancel(self, dict, *args, **kwargs):
        try:
            logs = (log.objects.all().filter(codigo=dict["code"])).order_by("-date")
            destino = str(logs[0].origem)
            create_log = log(codigo = dict["code"], origem = "Calibração", destino = destino , responsible = kwargs["Request"].user.username, observation="Cancelamento")
            create_log.save()
            equipment = Equipament.objects.get(codigo=dict["code"])
            equipment.in_calibration = 0
            equipment.position = destino
            equipment.save()
        except:
            return "Fail"
        return "Success"

    def to_return(self, dict,*args, **kwargs):
        try:
            if(dict["date"]!=''):
                 date = parse_date(dict["date"])
            else:
                date = datetime.today()
            create_log = log(codigo = dict["code"], origem = "Calibração", destino = base , responsible = kwargs["Request"].user.username)
            equipment = Equipament.objects.get(codigo= dict["code"])
            equipment.date_calibration = date
            equipment.in_calibration= 0
            equipment.position = base
            equipment.save_special()
            create_log.save()
        except:
            return "Fail"
        return "Success"
    

class Cars(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_move'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Cars, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **Kwargs):
        cars = Car.objects.all()
        context ={
            "where":"carros",
            "cars":cars
        }
        return render(request, 'carros.html', context)
    
    def post(self, request, *args, **kwargs):
        self.dinamic_templates = {
            "requestTemplate":self.get_template
        }
        json_request = json.loads(request.body)
        html = self.dinamic_templates[json_request["type"]](request,json_request)
        data = {
            "type":json_request["type"],
            "args":json_request["args"],
            "payloadHTML":html
        }
        return JsonResponse(data)
    def get_template(self, request, dict, *args, **kwargs):
        if(dict["args"][0]=="cars_free"):
            cars = Car.objects.all().filter(in_use=None)
        else:
            cars = Car.objects.all().exclude(in_use=None)
        context =Context({"cars":cars})
        template = open(ajax_template[dict["args"][0]],'r').read()
        print(template)
        a = Template(template).render(context)
        print(a)

def teste(request):
    print(request.body)
    return JsonResponse({"ok":"ok"})