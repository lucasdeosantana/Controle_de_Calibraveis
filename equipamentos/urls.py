"""equipamentos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CdC.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',do_login, name='home'),
    path('login/',do_login, name='login'),
    path('logout/', do_logout, name='logout'),
    path('move/',move.as_view(), name='move'),
    path('equipment/<slug:station>/',list_of_equips.as_view(), name='equipment'),
    path('super/<slug:page>/',superview.as_view()),
    path('CARS/', Cars.as_view(), name='cars'),
    path('log/<int:equipment>/', log_equips.as_view()),
    path('logcar/<slug:license>', log_car.as_view()),
]