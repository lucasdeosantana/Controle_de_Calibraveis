
from django.contrib import admin
from django.urls import path
from CdC.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AuthenticationLogin , name='home'),
    path('login/', AuthenticationLogin , name='login'),
    path('logout/', AuthenticationLogout, name='logout'),
    path('move/', MoveView.as_view(), name='move'),
    path('equipment/<slug:equipPlace>/', EquipmentView.as_view(), name='equipment'),
    path('Calibration/', CalibrationView.as_view()),
    path('CARS/', Cars.as_view(), name='cars'),
    path('log/<int:equipment>/', LogEquipView.as_view()),
    path('logcar/<slug:license>', LogCarView.as_view()),
    path('user/adduser/', AuthenticationAddUser.as_view()),
    path('user/edituser/', AuthenticationEditUser.as_view())
]