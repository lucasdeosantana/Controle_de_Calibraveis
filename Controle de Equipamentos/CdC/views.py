from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def login(request):
    print(request.POST)
    return render(request,'login.html')
def move(request):
    print(request.GET)
    return render(request,'move.html')
def ajx(request):
    data = {
        'Lucas':'Lindo'
    }
    return JsonResponse(data)