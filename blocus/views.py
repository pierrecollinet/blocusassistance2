# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context

from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required

from django.contrib.sitemaps import Sitemap

import json
import json as simplejson

from datetime import datetime, timedelta
from django.views.decorators.gzip import gzip_page

from htmlmin.decorators import minified_response

# import models
#from .models import Campus
from ba2.models import Campus
from blocus.models import ModuleBlocus, Blocus

# import forms
from blocus.forms import InscriptionBlocusModelForm

@minified_response
#@gzip_page
def inscription_blocus(request):
  form = InscriptionBlocusModelForm(request.POST or None)
  form.fields["module"].queryset = ModuleBlocus.objects.all()
  c = {'form':form}
  return render(request, 'inscription-blocus.html', c)

@minified_response
#@gzip_page
def blocus_assistes(request):
  c = {}
  return render(request, 'blocus-assistes.html', c)

@login_required
@minified_response
#@gzip_page
def confirmation_inscription(request):
  c = {}
  return render(request, 'confirmation-inscription.html', c)




# AJAX
def ajax_get_modules(request, pk):
    today = datetime.today()
    current_blocus = Blocus.objects.get(is_current=True)
    campus = Campus.objects.get(pk=pk)
    modules = ModuleBlocus.objects.filter(blocus=current_blocus, campus=campus, date_debut__gte=today).order_by('date_debut')
    modules_dict=[]
    [modules_dict.append((each_module.pk,each_module.get_name())) for each_module in modules]
    return HttpResponse(simplejson.dumps(modules_dict), content_type="application/json")

def ajax_calculate_price(request):
    if request.is_ajax():
        price = 0
        nombre_semaines = 0
        nombre_weekends = 0
        tarif_semaines = 0
        tarif_weekends = 0
        promo = request.GET['promo']
        for id in request.GET.getlist('module[]'):
            module = ModuleBlocus.objects.get(id=id)
            if module.sem_or_we == "sem":
                nombre_semaines += 1
                tarif_semaines += int(module.prix)
            elif module.sem_or_we == "we":
                nombre_weekends += 1
                tarif_weekends += int(module.prix)
            price += int(module.prix)
        # pas intégré pour l'instant
        # promo = CodePromo.objects.filter(
        #                                  date_fin_validite__gte = datetime.datetime.now(),
        #                                  code=promo,
        #                                  active = True
        #                                  )
        data = {
                "price":price,
                "nombre_weekends":nombre_weekends,
                "nombre_semaines":nombre_semaines,
                "tarif_semaines":tarif_semaines,
                "tarif_weekends":tarif_weekends,
                }
        return JsonResponse(data)
    else :
        raise Http404


