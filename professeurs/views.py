# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.template import Context

from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required

from django.contrib.sitemaps import Sitemap

import json
from datetime import datetime, timedelta, date

from django.views.decorators.gzip import gzip_page

from htmlmin.decorators import minified_response
from django.contrib import messages
from django.conf import settings

# import models
#from .models import Campus
from professeurs.models import Professeur, JourneeBlocusProf, RapportBlocusModule, RapportBlocusJournalier
from etudiants.models import Etudiant
from blocus.models import Blocus, ProfesseurBlocus,ModuleBlocus, Presence

#import forms
from professeurs.forms import ProfesseurModelForm, BlocusJourneeForm, ModifyBlocusJourneeForm, RapportBlocusJournalierModelForm, ModifierRapportBlocusJournalierModelForm
from etudiants.forms import EtudiantFullModelForm

@minified_response
#@gzip_page
def accueil(request):
  c = {}
  return render(request, 'professeurs/accueil.html', c)

def professeur_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated():
            return decorated_view_func(request)  # return redirect to signin
        if len(Professeur.objects.filter(user=request.user, active=True))==1:
            professeur = Professeur.objects.get(user=request.user)
            return function(request, *args, **kwargs)
        else:
            # redirect vers une page demandant de contacter un admin pour devenir actif
            return HttpResponseRedirect(reverse('completer-profil-prof'))
    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper

@professeur_required
@minified_response
#@gzip_page
def dashboard(request):
  professeur = request.user.professeur
  c = {'professeur':professeur}
  return render(request, 'professeurs/tableau-de-bord.html', c)

@minified_response
#@gzip_page
def complete_profile(request):
  if len(Professeur.objects.filter(user=request.user)) == 0 :
    form = ProfesseurModelForm(request.POST or None)
    if form.is_valid():
      # On sauve un nouvel étudiant
      professeur = form.save(commit=False)
      user = request.user
      professeur.user = user
      professeur.save()

      # On update les infos de ce user
      user.first_name = professeur.prenom
      user.last_name = professeur.nom
      user.save

      # On prévient les fondateurs
      plaintext = get_template('../templates/emails/nouveau-prof-alert-fondateurs.txt')
      htmly     = get_template('../templates/emails/nouveau-prof-alert-fondateurs.html')
      subject, from_email = "Nouvelle inscription professeur - " + professeur.prenom + ' ' + professeur.nom, professeur.email
      to = settings.EMAILS
      d = { 'professeur': professeur}
      text_content = plaintext.render(d)
      html_content = htmly.render(d)
      msg = EmailMultiAlternatives(subject, text_content, from_email, to)
      msg.attach_alternative(html_content, "text/html")
      msg.send()

      c = { 'message': "Nous revenons vers toi dans les plus brefs délais"}
      return render(request, 'professeurs/thanks.html', c)
    c = {'form':form}
    return render(request, 'professeurs/completer-profil.html', c)
  else :
    return HttpResponseRedirect(reverse('voir-profil-prof', kwargs={'pk':request.user.professeur.pk}))

@professeur_required
@minified_response
#@gzip_page
def show_profile(request, pk):
  professeur = Professeur.objects.get(pk=pk)
  c = {'professeur':professeur}
  return render(request, 'professeurs/voir-profil.html', c)

@professeur_required
@minified_response
#@gzip_page
def show_student(request, pk):
  etudiant = Etudiant.objects.get(pk=pk)
  c = {'etudiant':etudiant}
  return render(request, 'professeurs/show_student.html', c)

@professeur_required
@minified_response
#@gzip_page
def complete_profile_student(request, pk):
  etudiant = Etudiant.objects.get(pk=pk)
  form = EtudiantFullModelForm(request.POST or None , request.FILES or None, instance = etudiant)
  if form.is_valid():
    form.save()
    if request.POST and 'suivi' in request.POST and request.POST['suivi']=='oui':
      current_module = ModuleBlocus.objects.filter(date_debut__lte=date.today(), date_fin__gte=date.today(), blocus=Blocus.objects.filter(is_current=True).first()).first()
      if len(RapportBlocusModule.objects.get_or_create(module=current_module, etudiant=etudiant, auteur=request.user.professeur)) ==0:
        rapportmodule = RapportBlocusModule.create(
                                          module=current_module,
                                          etudiant=etudiant,
                                          auteur=request.user.professeur
                                          )
    if 'next_url' in request.POST :
      return HttpResponseRedirect(request.POST['next_url'])
    return redirect("tableau-de-bord-professeurs")
  c = {'etudiant':etudiant, 'form':form}
  if request.GET and 'next_url' in request.GET :
    c.update({'next_url':request.GET['next_url']})
  return render(request, 'professeurs/completer_profil_etudiant.html', c)

@professeur_required
@minified_response
#@gzip_page
def modify_profile(request):
  form = ProfesseurModelForm(request.POST or None, instance = request.user.professeur)
  if form.is_valid():
    form.save()
    messages.success(request, 'Profil mis à jour')
    return HttpResponseRedirect(reverse('voir-profil-prof', kwargs={'pk':request.user.professeur.pk}))
  c = {'form':form}
  return render(request, 'professeurs/modifier-profil.html', c)

@professeur_required
@minified_response
def encoder_journee_blocus(request):
  blocus = Blocus.objects.filter(is_current=True).first()
  campus_for_this_teacher = ProfesseurBlocus.objects.filter(blocus = blocus).first().campus.all()
  form =BlocusJourneeForm(request.POST or None, request=request, initial={'campus': campus_for_this_teacher.first()})
  form.fields["campus"].queryset = campus_for_this_teacher
  if form.is_valid():
    journee_blocus = form.save(commit=False)
    journee_blocus.professeur = request.user.professeur
    journee_blocus.blocus = blocus
    journee_blocus.save()
    return redirect("detail-blocus", pk=blocus.pk)
  c = {'form' : form}
  return render(request, "professeurs/journee-blocus/encoder-journee-blocus.html", c)


@professeur_required
@minified_response
def modifier_journee_blocus(request, pk):
  journee_blocus = JourneeBlocusProf.objects.get(pk=pk)
  blocus = Blocus.objects.filter(is_current=True).first()
  campus_for_this_teacher = ProfesseurBlocus.objects.filter(blocus = blocus).first().campus.all()
  form =ModifyBlocusJourneeForm(request.POST or None, request=request, instance = journee_blocus )
  form.fields["campus"].queryset = campus_for_this_teacher
  if form.is_valid():
    form.save()
    return redirect("detail-blocus", pk=journee_blocus.blocus.pk)
  c = {'journee_blocus':journee_blocus, 'form':form}
  return render(request, "professeurs/journee-blocus/modifier-journee-blocus.html", c)

@professeur_required
@minified_response
def supprimer_journee_blocus(request, pk):
  journee_blocus = JourneeBlocusProf.objects.get(pk=pk)
  c = {'journee_blocus':journee_blocus}
  if request.POST :
    if journee_blocus.is_paid :
      error_msg = "Désolé mais tu as déjà été rémunéré pour cette journée. Contacte les administrateurs si nécessaire"
      c.update({'error_msg':error_msg})
    else :
      journee_blocus.delete()
      return redirect("detail-blocus", pk=journee_blocus.blocus.pk)
  return render(request, "professeurs/journee-blocus/supprimer-journee-blocus.html", c)


@professeur_required
@minified_response
def suivi_journalier_blocus(request, pk):
  presence = Presence.objects.get(pk=pk)
  form = RapportBlocusJournalierModelForm(request.POST or None)
  if form.is_valid():
    rapport = form.save(commit=False)
    rapport.presence = presence
    rapport.auteur = request.user.professeur
    rapport.date = presence.date
    rapport.rapportmodule = presence.etudiant.get_suivi_actuel(presence.date)
    rapport.save()
    return redirect("grille-suivi-etudiants", pk_campus=presence.jourblocus.campus.pk, pk_module=rapport.rapportmodule.module.pk)
  c = {'presence':presence, 'form':form}
  if request.GET and 'module' in request.GET :
    c.update({'module_id':request.GET['module']})
  return render(request, "professeurs/suivi-journalier/suivi-journalier-blocus.html", c)

@professeur_required
@minified_response
def voir_suivi_journalier(request, pk):
  rapport = RapportBlocusJournalier.objects.get(pk=pk)
  c = {'rapport':rapport}
  return render(request, "professeurs/suivi-journalier/voir-suivi-journalier.html", c)

@professeur_required
@minified_response
def modifier_suivi_journalier(request, pk):
  rapport = RapportBlocusJournalier.objects.get(pk=pk)
  form = ModifierRapportBlocusJournalierModelForm(request.POST or None, instance = rapport)
  if form.is_valid():
    rapport = form.save(commit=False)
    rapport.statut = "bilan_realise"
    rapport.save()
    if 'enregistrer_and_email' in request.POST and rapport.statut == "bilan_realise":
        # Il faut envoyer un email aux parents
        "ENVOYER EMAIL + PDF"
        rapport.statut = "rapport_envoye"
        rapport.save()
    if rapport.presence.date == rapport.rapportmodule.module.date_fin :
      return redirect("grille-suivi-etudiants", pk_campus=rapport.presence.jourblocus.campus.pk, pk_module=rapport.rapportmodule.module.pk)
    else :
      date_demain = rapport.presence.date + timedelta(days=1)
      presence = Presence.objects.filter(etudiant = rapport.presence.etudiant, date = date_demain).first()
      return redirect("suivi-journalier-blocus", pk=presence.pk)
  c = {'rapport':rapport, 'form':form}
  return render(request, "professeurs/suivi-journalier/modifier-suivi-journalier.html", c)

def display_rapport_journalier(request, pk):
  rapport = RapportBlocusJournalier.objects.get(pk=pk)
  c = {'rapport':rapport}
  return render(request, "professeurs/suivi-journalier/pdf/display-rapport-journalier.html", c)

def send_rapport_journalier(request, pk):
  htmly     = get_template('../templates/emails/rapport-journalier.html')
  subject, from_email = 'Journée de blocus du ' + rapport.date + ' - ' + rapport.presence.etudiant.prenom + ' ' + rapport.presence.etudiant.nom, 'info@blocusassistance.be'
  to = settings.EMAILS

  c={ 'pagesize':'A4' }
  d = Context(c)
  html_content = htmly.render(d)
  text_content = plaintext.render(d)
  msg = EmailMultiAlternatives(subject,text_content, from_email, to)
  msg.attach_alternative(html_content, "text/html")
  # create an API client instance
  client = pdfcrowd.Client(settings.USERNAME_PDFCROW, settings.API_KEY_PDFCROWD)
  # convert a web page and store the generated PDF to a variable
  pdf = client.convertURI(reverse('display-rapport-journalier', args={pk}))

  msg.attach('rapport-blocus.pdf', pdf, 'application/pdf')
  msg.content_subtype = "html"
  msg.send()
  return render(request, "professeurs/suivi-journalier/pdf/display-rapport-journalier.html", c)
