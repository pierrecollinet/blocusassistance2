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
from django.conf import settings
import json
import json as simplejson

from datetime import datetime, timedelta
from django.views.decorators.gzip import gzip_page

from htmlmin.decorators import minified_response

from django.db.models import Q

# import models
#from .models import Campus
from ba2.models import Campus
from blocus.models import ModuleBlocus, Blocus, InscriptionBlocus,PresenceJourBlocus, ProfesseurBlocus
from etudiants.models import Etudiant
from billing.models import BillingProfile
from professeurs.models import JourneeBlocusProf,RapportBlocusModule

# import forms
from blocus.forms import InscriptionBlocusModelForm,InscriptionBlocusModelFormByTeacher, PresenceModelForm, Presence, SearchForm

from etudiants.views import etudiant_required
from professeurs.views import professeur_required


import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY")
stripe.api_key = STRIPE_SECRET_KEY

@etudiant_required
@minified_response
#@gzip_page
def inscription_blocus(request):
  form = InscriptionBlocusModelForm(request.POST or None, request=request)
  form.fields["module"].queryset = ModuleBlocus.objects.all()
  if form.is_valid():
    new_inscription = form.save(commit=False)
    new_inscription.etudiant = request.user.etudiant
    new_inscription.blocus = Blocus.objects.filter(is_current = True).first()
    # Si cet étudiant a déjà une inscription, on l'update
    if len(InscriptionBlocus.objects.filter(blocus = new_inscription.blocus, etudiant = request.user.etudiant, campus = form.cleaned_data['campus']))>0 :
      inscription = InscriptionBlocus.objects.get(blocus = new_inscription.blocus, etudiant = request.user.etudiant, campus = form.cleaned_data['campus'])
      for mod in form.cleaned_data['module']:
        inscription.module.add(mod)
      inscription.save()
      inscription.montant = inscription.calculate_total_price()
      inscription.save()
      new_inscription = inscription
    # Sinon, on crée une nouvelle
    else :
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
  current_blocus = Blocus.objects.filter(is_current = True)
  if len(current_blocus) == 1:
    current_blocus = current_blocus.first()
    c.update({'current_blocus':current_blocus})
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

    # Si c'est déjà payé, on ne facture pas une deuxième fois !
    if inscription_obj.is_paid :
      return redirect("confirmation-inscription-blocus")

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
          # On prévient les fondateurs
          plaintext = get_template('../templates/emails/confirmation-inscription-paiement-online.txt')
          htmly     = get_template('../templates/emails/confirmation-inscription-paiement-online.html')
          subject, from_email = "Inscription au blocus assisté - "+inscription_obj.etudiant.prenom+inscription_obj.etudiant.nom , 'info@blocusassistance.be'
          to = settings.EMAILS
          d = {'inscription':inscription_obj}
          text_content = plaintext.render(d)
          html_content = htmly.render(d)
          msg = EmailMultiAlternatives(subject, text_content, from_email, to)
          msg.attach_alternative(html_content, "text/html")
          msg.send()
          return redirect("confirmation-inscription-blocus")
        else:
          print(crg_msg)
          return redirect("blocus:checkout")
      elif 'payer-par-virement' in request.POST :
        # On prévient les fondateurs
        plaintext = get_template('../templates/emails/confirmation-inscription-virement.txt')
        htmly     = get_template('../templates/emails/confirmation-inscription-virement.html')
        subject, from_email = "Inscription au blocus assisté - "+inscription_obj.etudiant.prenom+inscription_obj.etudiant.nom , 'info@blocusassistance.be'
        to = settings.EMAILS
        d = {'inscription':inscription_obj}
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        print(to)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return redirect("confirmation-inscription-blocus")
    context = {
        "object": inscription_obj,
        "inscription": inscription_obj,
        "billing_profile": billing_profile,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
    }
    return render(request, "checkout.html", context)

@professeur_required
@minified_response
def imprimer_planning(request, pk_campus, pk_module):
  campus = Campus.objects.get(pk = pk_campus)
  module = ModuleBlocus.objects.get(pk = pk_module)
  today = date.today()
  inscriptions = InscriptionBlocus.objects.filter(campus=campus, module=module).order_by('etudiant__prenom')
  joursblocus = PresenceJourBlocus.objects.filter(campus=campus,
                                                    blocus=Blocus.objects.get(is_current=True),
                                                    date__gte=module.get_date_debut(),
                                                    date__lte=module.get_date_fin()
                                                  )
  c = {'inscriptions':inscriptions,'module':module,'joursblocus':joursblocus, 'today':today, 'campus':campus}
  return render(request, "professeurs/presence/imprimer-presence.html", c)

from datetime import date
@professeur_required
@minified_response
def cocher_presence(request, pk_campus, pk_module):
  campus = Campus.objects.get(pk = pk_campus)
  module = ModuleBlocus.objects.get(pk = pk_module)
  today = date.today()
  inscriptions = InscriptionBlocus.objects.filter(campus=campus, module=module).order_by('etudiant__prenom')
  joursblocus = PresenceJourBlocus.objects.filter(campus=campus,
                                                    blocus=Blocus.objects.get(is_current=True),
                                                    date__gte=module.get_date_debut(),
                                                    date__lte=module.get_date_fin()
                                                  )
  if request.POST :
    for jour in joursblocus.filter(date=today):
        for presence in jour.presence_set.all():
            presence.statut = 'absent'
            presence.save()
    presence_ids = request.POST.getlist('presence_id')
    print(presence_ids)
    for id in presence_ids:
        presence = Presence.objects.get(id=id)
        presence.statut = 'present'
        presence.save()
  c = {'inscriptions':inscriptions,'module':module,'joursblocus':joursblocus, 'today':today, 'campus':campus}
  return render(request, "professeurs/presence/cocher-presence.html", c)

@professeur_required
@minified_response
def grille_suivi_etudiants(request, pk_campus, pk_module):
  campus = Campus.objects.get(pk = pk_campus)
  module = ModuleBlocus.objects.get(pk = pk_module)
  today = date.today()
  etudiant_with_rapports_ids = RapportBlocusModule.objects.filter(module=module).values_list('etudiant', flat=True)
  inscriptions = InscriptionBlocus.objects.filter(campus=campus, module=module, etudiant__id__in=etudiant_with_rapports_ids).order_by('etudiant__prenom')
  joursblocus = PresenceJourBlocus.objects.filter(campus=campus,
                                                    blocus=Blocus.objects.get(is_current=True),
                                                    date__gte=module.get_date_debut(),
                                                    date__lte=module.get_date_fin()
                                                  )
  c = {'inscriptions':inscriptions,'module':module,'joursblocus':joursblocus, 'today':today, 'campus':campus}
  return render(request, "professeurs/presence/grille-suivi-etudiants.html", c)


@professeur_required
def detail_presence(request, pk, pk_module):
  presence = Presence.objects.get(pk = pk)
  form = PresenceModelForm(request.POST or None, instance = presence)
  if form.is_valid():
    form.save()
    pk_module = request.POST['pk_module']
    pk_campus = request.POST['pk_campus']
    return redirect("cocher-presence", pk_campus = pk_campus, pk_module = pk_module)
  return render(request, 'professeurs/presence/detail_presence.html', {'presence':presence,'form':form, 'pk_module':pk_module})



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


@professeur_required
@minified_response
#@gzip_page
def detail_blocus(request, pk):
  today = date.today()
  blocus = Blocus.objects.get(pk=pk)
  profblocus = ProfesseurBlocus.objects.filter(blocus=blocus, professeur=request.user.professeur).first()
  campus_for_this_prof = profblocus.campus.all()
  inscriptions = InscriptionBlocus.objects.filter(blocus=blocus, campus__in=campus_for_this_prof)
  form = SearchForm(request.POST or None)
  journees_blocus = JourneeBlocusProf.objects.filter(professeur=request.user.professeur, blocus=blocus).order_by('date')
  prof_blocus = ProfesseurBlocus.objects.filter(professeur=request.user.professeur, blocus=blocus).first()
  if request.GET and 'search' in request.GET :
    search_field = request.GET['search']

    inscriptions = inscriptions.filter(Q(etudiant__prenom__icontains = search_field)|Q(etudiant__nom__icontains = search_field))
  c = {'blocus':blocus, 'inscriptions':inscriptions, 'campus_for_this_prof':campus_for_this_prof, 'form':form, 'today':today,'prof_blocus':prof_blocus, 'journees_blocus': journees_blocus}
  return render(request, 'detail_blocus.html', c)

@professeur_required
@minified_response
#@gzip_page
def display_list_student(request, pk_campus, pk_module):
  campus = Campus.objects.get(pk = pk_campus)
  module = ModuleBlocus.objects.get(pk = pk_module)
  today = date.today()
  inscriptions = InscriptionBlocus.objects.filter(campus=campus, module=module).order_by('etudiant__prenom')
  c = {'inscriptions':inscriptions,'module':module, 'campus':campus}
  return render(request, "professeurs/presence/liste-etudiants-par-module.html", c)


@professeur_required
@minified_response
#@gzip_page
def ajout_etudiant(request):
  form = InscriptionBlocusModelFormByTeacher(request.POST or None, request=request)
  if request.GET and 'etudiant' in request.GET :
      form = InscriptionBlocusModelFormByTeacher(request.POST or None, request=request, initial={'etudiant':Etudiant.objects.get(id=request.GET['etudiant'])})
  etudiants = Etudiant.objects.all()
  if form.is_valid():
    inscription = form.save(commit=False)
    etudiant = request.POST['etudiant']
    blocus = Blocus.objects.filter(is_current = True).first()
    campus = form.cleaned_data['campus']

    # si l'inscirption existe déjà, on la crée
    if len(InscriptionBlocus.objects.filter(blocus       = blocus, etudiant = etudiant, campus = campus))>0 :
      inscription = InscriptionBlocus.objects.get(blocus = blocus, etudiant = etudiant, campus = campus)
      for mod in form.cleaned_data['module']:
        inscription.module.add(mod)
      inscription.save()
      inscription.montant = inscription.calculate_total_price()
      inscription.save()
    # Sinon, on crée une nouvelle
    else :
      inscription.montant = 0
      inscription.blocus = blocus
      inscription.save()
      inscription.module = form.cleaned_data['module']
      inscription.save()
      inscription.montant = inscription.calculate_total_price()
      inscription.suivi_inscription += "-->Ajouté manuellement par "+ request.user.professeur.prenom + " " + request.user.professeur.nom
    inscription.save()
    next_url = request.POST['next_url']
    return HttpResponseRedirect(next_url)
  c = {'form':form, 'etudiants':etudiants}
  if request.GET and 'next_url' in request.GET :
    next_url = request.GET['next_url']
    c.update({'next_url':next_url})
  return render(request, "professeurs/presence/ajout-etudiant.html", c)

def ajax_get_students_list(request, string):
  search_field = string
  students = Etudiant.objects.filter(Q(prenom__icontains = search_field)|Q(nom__icontains = search_field))
  if len(students) == 0 :
    students = Etudiant.objects.all()
  students_dict = []
  [students_dict.append((each_student.pk,each_student.prenom + ' ' + each_student.nom)) for each_student in students]
  return HttpResponse(simplejson.dumps(students_dict), content_type="application/json")

def enquete_satisfaction_blocus(request, pk_campus, pk_module):
  campus = Campus.objects.get(pk = pk_campus)
  module = ModuleBlocus.objects.get(pk = pk_module)
  c = {"campus":campus, "module":module}
  return render(request, "feedback.html", c)
