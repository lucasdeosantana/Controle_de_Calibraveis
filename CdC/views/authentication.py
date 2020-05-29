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
            "places":Place.objects.all()
        }
        return render(request, 'user/adduser.html', context)