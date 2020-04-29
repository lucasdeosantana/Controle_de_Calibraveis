from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
# Create your views here.
def login(request):
    print(request.POST)
    return render(request,'login.html')

class move(View):
    def get(self, request, *args, **Kwargs):
        return render(request,'move.html')
    @csrf_exempt
    def post(self, request, *args, **Kwargs):
        print(request.body)
        return HttpResponse("ok")
def ajx(request):
    data = {
        'Lucas':'Lindo'
    }
    return JsonResponse(data)