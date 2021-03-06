from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.views import View
from CdC.models import Log, Place, Carlog
import os
from equipamentos.settings import BASE_DIR
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class LogEquipView(PermissionRequiredMixin, View):
	template_name = "login.html"
	permission_required = 'CdC.can_move'

	def get(self, request, equipment, *args, **kwargs):
		logs = (Log.objects.all().filter(code=equipment)).order_by("-date")
		page = request.GET.get('page',1)
		paginator = Paginator(logs, 40)
		try:
			logs_pag = paginator.page(page)
		except PageNotAnInteger:
			logs_pag = paginator.page(1)
		except EmptyPage:
			logs_pag = paginator.page(paginator.num_pages)
		context = {
			"logs":logs_pag,
			"places":Place.objects.all()
			}
		return render(request, 'log/log.html', context)

class LogCarView(PermissionRequiredMixin, View):
	template_name = "login.html"
	permission_required = 'CdC.can_move'

	def get(self, request, license, *args, **kwargs):
		logs = (Carlog.objects.all().filter(licensePlate=license.lower())).order_by("-date")
		page = request.GET.get('page',1)
		paginator = Paginator(logs, 40)
		try:
			logs_pag = paginator.page(page)
		except PageNotAnInteger:
			logs_pag = paginator.page(1)
		except EmptyPage:
			logs_pag = paginator.page(paginator.num_pages)
		context = {
			"logs":logs_pag,
			"places":Place.objects.all()
			}
		return render(request, 'log/logcar.html', context)