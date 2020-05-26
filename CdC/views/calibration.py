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
base = Place.objects.get(name="Base")

class CalibrationView(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_move'


    def get(self, request, *args, **Kwargs):
        equips_for_calibration = (Equipment.objects.all().filter(in_calibration=1)).order_by('date_validity')
        context = {
            "equipments":equips_for_calibration,
            "where":"Calibration",
            "places":Place.objects.all()
        }
        return render(request, "Calibration.html", context)



    def post(self, request, *args, **kwargs):
        self.functs ={
            "equipConfirm":self.get_Equipment_to_Confirm,
            "equipBack":self.get_Equipment_to_back,
            "to_confirm":self.to_confirm,
            "to_cancel":self.to_cancel,
            "to_return":self.to_return
        }
        json_request = json.loads(request.body)
        table= self.functs[json_request["type"]](json_request, request=request)
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


    def get_Equipment_to_Confirm(self, *args, **kwargs):
        equips_for_calibration = (Equipment.objects.all().filter(in_calibration=1)).order_by('date_validity')
        template = Template("""
            {% for equipment in equipments %}
            <tr class="bg" id="{{ equipment.code }}">
                <th scope="row"><a {% if perms.CdC.can_see_log %}href="/log/{{ equipment.code }}"{% endif %}>{{ equipment.code }}</a></th>
                <td>{{ equipment.date_validity|date:"F/Y" }}</td>
                <td>{{ equipment.name }}</td>
                <td><button class="btn btn-primary" onclick="button_received({{ equipment.code }}, 'btn_confirm')"><i class="fa fa-check"></i></button><button
                    class="btn btn-danger" onclick="button_received({{ equipment.code }}, 'btn_cancel')"><i class="fa fa-times"></i></button></td>
            </tr>
            {% endfor %}""")
        context = Context({"equipments":equips_for_calibration, "perms":kwargs["request"].user})
        #print(template.render(context))
        return template.render(context)


    def get_Equipment_to_back(self, *args, **kwargs):
        equips_for_calibration = (Equipment.objects.all().filter(in_calibration=2)).order_by('date_validity')
        template = Template("""
            {% if equipments %}
            {% for equipment in equipments %}
            <tr class="bg" id="{{ equipment.code }}">
                <th scope="row">{{ equipment.code }}</th>
                <td><input type="date" id="d{{ equipment.code }}"></td>
                <td>{{ equipment.name }}</td>
                <td><button class="btn btn-primary" onclick="button_received({{ equipment.code }}, 'btn_return')"><i class="fas fa-undo"></i></button></td>
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
            equipment = Equipment.objects.get(code=dict["code"])
            equipment.in_calibration = 2
            equipment.move(origin = Place.objects.get(name="Base"), user = kwargs["request"].user, typeLog=3)
        except:
            return "Fail"
        return "Success"


    def to_cancel(self, dict, *args, **kwargs):
        try:
            logs = (Log.objects.all().filter(code=dict["code"])).order_by("-date")
            print(logs[0].origin)
            equipment = Equipment.objects.get(code=dict["code"])
            equipment.where = logs[0].origin
            equipment.in_calibration = 0
            equipment.move(origin = Place.objects.get(name="Base"), user = kwargs["request"].user, typeLog=5)
        except:
            return "Fail"
        return "Success"


    def to_return(self, dict,*args, **kwargs):
        try:
            if(dict["date"]!=''):
                 date = parse_date(dict["date"])
            else:
                date = datetime.today()            
            equipment = Equipment.objects.get(code=dict["code"])
            equipment.date_calibration = date
            equipment.in_calibration= 0
            equipment.where = Place.objects.get(name="Base")
            equipment.save_special(origin = Place.objects.get(name="Base"), user = kwargs["request"].user, typeLog=4)
        except:
            return "Fail"
        return "Success"