from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
import json
from .models import *

base = "Faria Lima"
# Create your views here.
def login(request):
    print(request.POST)
    return render(request,'login.html')


class move(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(move, self).dispatch(request, *args, **kwargs)
        
    def get(self, request, *args, **Kwargs):
        return render(request,'move.html')

    def post(self, request, *args, **Kwargs):
        self.functs={
            "doMove":self.do_move,
            "request":self.get_equipament
        }
        json_request = json.loads(request.body)
        answer = self.functs[json_request["type"]](json_request)
        return JsonResponse(answer)
    def get_equipament(self,data):
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
    def do_move(self, data):
        if(data["equipmentCode"].isnumeric()):
            equipment = Equipament.objects.get(codigo=data["equipmentCode"])
            if(data["for"]== "Calibração"):
                equipment.in_calibration = 1
                equipment.position = base
            else:
                equipment.position = data["for"]
            create_log = log(codigo = data["equipmentCode"], origem = data["where"], destino = data["for"], responsible = "lucas")
            create_log.save()
            equipment.log.add(create_log)
            equipment.save()
            data = {"type":"Success"}
        else:
            car = Car.objects.get(placa=data["equipmentCode"])
            logcar = carlog(placa=data["equipmentCode"], origem = data["where"], destino = data["for"], responsible = "lucas")
            logcar.save()
            car.position = data["for"]
            car.log.add(logcar)
            car.save()
            data = {"type":"Success"}
        return data