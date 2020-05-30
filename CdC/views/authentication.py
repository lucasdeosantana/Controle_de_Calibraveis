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
from django.contrib.auth.models import User, Group
from CdC.models import *
from django.core import serializers

def AuthenticationLogin(request, *args, **kwargs):
    if request.method == 'POST':
        user = authenticate(username=request.POST['user'], password=request.POST['pass'])
        if user is not None:
            login(request, user)
            return redirect("/move")
    return render(request, 'user/login.html')

def AuthenticationLogout(request, *args, **kwargs):
    logout(request)
    return redirect("/login/")

class AuthenticationAddUser(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_move'
    def get(self, request, *args, **Kwargs):
        context = {
            "places":Place.objects.all(),     
        }
        return render(request, 'user/adduser.html', context)
    def post(self, request, *args, **kwargs):
        json_request = json.loads(request.body)
        if json_request["type"] == 'createuser':
            try:
                json_payload=json_request["payload"]
                user = User.objects.create_user(username=json_payload["username"],
                email=json_payload["email"], password="123456a@",
                first_name=json_payload["name"], last_name=json_payload["workPlace"])
                user.groups.add(Group.objects.get(name=json_payload["permissions"]))
                response={
                    "type":json_request["type"],
                    "status":"success"
                }
            except:
                response={
                    "type":json_request["type"],
                    "status":"fail"
                }
        return JsonResponse(response)

class AuthenticationEditUser(PermissionRequiredMixin, View):
    template_name = "login.html"
    permission_required = 'CdC.can_manager_user'
#---------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        self.functions = {
            "search":self.get_user_by_username,
            "edituser":self.edit_user
        }
        super(AuthenticationEditUser, self).__init__(*args, **kwargs)
#---------------------------------------------------------------------------------
    def get(self, request, *args, **Kwargs):
        context = {
            "places":Place.objects.all(),
        }
        return render(request, 'user/edituser.html', context)
#---------------------------------------------------------------------------------        
    def post(self, request, *args, **kwargs):
        json_request = json.loads(request.body)
        data=self.functions[json_request["type"]](request, json_request)
        return JsonResponse(data)
#---------------------------------------------------------------------------------
    def get_user_by_username(self, request, json_request, *args, **kwargs):
        fields=serializers.serialize('json', 
            User.objects.all().filter(username=json_request["payload"]["username"]),
            fields=('first_name', 'last_name', 'email', 'groups', "is_active"))
        print(type(fields))
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
    def edit_user(self, request, json_request, *args, **kwargs):
        print(json_request)
        try:
            json_payload=json_request["payload"]
            user = User.objects.get(username=json_payload["username"])
            user.first_name=json_payload["name"]
            user.last_name=json_payload["workPlace"]
            user.email=json_payload["email"]
            if(json_payload["passwordReset"]): user.set_password("123456a@")
            user.groups.clear()
            user.groups.add(Group.objects.get(name=json_payload["permissions"]))
            user.is_active=json_payload["isactive"]
            user.save()
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