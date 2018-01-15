# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
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
from blocus.models import ModuleBlocus, Blocus, InscriptionBlocus
from etudiants.models import Etudiant
from billing.models import BillingProfile

# import forms
from blocus.forms import InscriptionBlocusModelForm

from etudiants.views import etudiant_required

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY")
stripe.api_key = STRIPE_SECRET_KEY

@etudiant_required
@minified_response
#@gzip_page
def inscription_blocus(request):
  form = InscriptionBlocusModelForm(request.POST or None)
  form.fields["module"].queryset = ModuleBlocus.objects.all()
  if form.is_valid():
    new_inscription = form.save(commit=False)
    new_inscription.etudiant = request.user.etudiant
    new_inscription.blocus = Blocus.objects.filter(is_current = True).first()
    new_inscription.montant = 0
    new_inscription.save()
    new_inscription.module = form.cleaned_data['module']
    new_inscription.save()
    new_inscription.montant = new_inscription.calculate_total_price()
    new_inscription.save()
    c = {'inscription':new_inscription}
    return redirect('checkout', pk = new_inscription.pk)
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

@login_required
def checkout(request, pk):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    has_card = False
    inscription_obj = InscriptionBlocus.objects.get(id = pk)
    if billing_profile is not None:
      has_card = billing_profile.has_card
    if request.method == "POST":
      inscription_id = request.POST["inscription_id"]
      inscription_obj = InscriptionBlocus.objects.get(id = inscription_id)
      if 'payer-en-ligne' in request.POST :
        did_charge, crg_msg = billing_profile.charge(inscription_obj)
        if did_charge:
          inscription_obj.is_paid = True
          inscription_obj.save()
          return redirect("confirmation-inscription-blocus")
        else:
          print(crg_msg)
          return redirect("blocus:checkout")
      elif 'payer-par-virement' in request.POST :
        # gérer l'inscription
        # - mail de confirmation
        # - rediriger vers une page de remerciement
        print('payer par virement')


    context = {
        "object": inscription_obj,
        "inscription": inscription_obj,
        "billing_profile": billing_profile,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
    }
    return render(request, "checkout.html", context)





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


