# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.template import Context

from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.sitemaps import Sitemap

import json
from datetime import datetime, timedelta
from django.views.decorators.gzip import gzip_page

from htmlmin.decorators import minified_response

from coursparticuliers.forms import CoursParticuliersModelForm, CoursParticuliersUserModelForm

@minified_response
#@gzip_page
def accueil(request):
  c = {}
  return render(request, 'cours-particuliers/accueil.html', c)

@minified_response
#@gzip_page
def inscription_cp(request):
  if request.user.is_authenticated():
    form = CoursParticuliersUserModelForm(request.POST or None)
    if form.is_valid():
      demande = form.save(commit=False)
      demande.email_contact = request.user.etudiant.email
      demande.tel_contact = request.user.etudiant.gsm
      demande.user = request.user
      demande.save()
      send_confirmation(demande)
      c = {'main_title':'Demande de cours particuliers', 'title': "Nous avons bien reçu votre demande",'texte': "Le responsable pédagogique prendra contact avec vous dans les plus brefs délais"}
      return render(request, "cours-particuliers/confirmation.html", c)
  else :
    form = CoursParticuliersModelForm(request.POST or None)
    if form.is_valid():
      demande = form.save()
      send_confirmation(demande)
      return redirect("confirmation-demande-cours")
  c = {'form':form}
  return render(request, 'cours-particuliers/inscription.html', c)

def send_confirmation(demande):
  # On prévient les fondateurs
  plaintext = get_template('../templates/emails/confirmation-demande-cp.txt')
  htmly     = get_template('../templates/emails/confirmation-demande-cp.html')
  subject, from_email = "Demande de cours particuliers - "+demande.matiere, 'info@blocusassistance.be'
  to = settings.EMAILS
  d = {'inscription':inscription_obj}
  text_content = plaintext.render(d)
  html_content = htmly.render(d)
  msg = EmailMultiAlternatives(subject, text_content, from_email, to)
  msg.attach_alternative(html_content, "text/html")
  msg.send()



