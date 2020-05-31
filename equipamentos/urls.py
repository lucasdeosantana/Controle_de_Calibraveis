
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
    path('Calibration/', CalibrationView.as_view(), name="calibration"),
    path('CARS/', Cars.as_view(), name='cars'),
    path('log/<int:equipment>/', LogEquipView.as_view()),
    path('log/<slug:license>', LogCarView.as_view(), name="log"),
    path('edit/adduser/', AuthenticationAddUser.as_view(), name="addUser"),
    path('edit/edituser/', AuthenticationEditUser.as_view(), name="editUser"),
    path('edit/editequip/', EquipmentEdit.as_view(), name="editEquipment"),
    path('edit/editcar/', CarEdit.as_view(), name="editCar"),
    path('edit/addequip/', EquipmentAdd.as_view(), name="addEquipment"),
    path('edit/addcar/', CarAdd.as_view(), name="addCar"),
]