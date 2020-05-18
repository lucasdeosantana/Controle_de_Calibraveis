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
base = "Base"
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
                <th scope="row"><a {% if perms.CdC.can_see_log %}href="/log/{{ equipment.codigo }}"{% endif %}>{{ equipment.codigo }}</a></th>
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
<<<<<<< HEAD
        create_log = log(codigo = dict["code"], origem = "Calibração", destino = "Calibração", responsible = kwargs["Request"].user.username, type_of_log=3)
=======
        create_log = log(codigo = dict["code"], origem = "Calibração", destino = "Calibração", responsible = kwargs["Request"].user.username)
>>>>>>> Uso_Geral
        create_log.save()
        return "Success"
    def to_cancel(self, dict, *args, **kwargs):
        try:
            logs = (log.objects.all().filter(codigo=dict["code"])).order_by("-date")
            destino = str(logs[0].origem)
<<<<<<< HEAD
            create_log = log(codigo = dict["code"], origem = "Calibração", destino = destino , responsible = kwargs["Request"].user.username, observation="Cancelamento", type_of_log=5)
=======
            create_log = log(codigo = dict["code"], origem = "Calibração", destino = destino , responsible = kwargs["Request"].user.username, observation="Cancelamento")
>>>>>>> Uso_Geral
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
<<<<<<< HEAD
            create_log = log(codigo = dict["code"], origem = "Calibração", destino = base , responsible = kwargs["Request"].user.username, type_of_log=4)
=======
            create_log = log(codigo = dict["code"], origem = "Calibração", destino = base , responsible = kwargs["Request"].user.username)
>>>>>>> Uso_Geral
            equipment = Equipament.objects.get(codigo= dict["code"])
            equipment.date_calibration = date
            equipment.in_calibration= 0
            equipment.position = base
            equipment.save_special()
            create_log.save()
        except:
            return "Fail"
        return "Success"