# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render,  redirect
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

from suiviintensif.forms import SuiviIntensifContactModelForm


@minified_response
#@gzip_page
def accueil(request):
  c = {}
  return render(request, 'suivi-intensif/accueil.html', c)

@minified_response
#@gzip_page
def inscription_suiviintensif(request):
  form = SuiviIntensifContactModelForm(request.POST or None)
  if form.is_valid():
    demande = form.save()
    # On prévient les fondateurs
    plaintext = get_template('../templates/emails/confirmation-demande-info-suivi-intensif.txt')
    htmly     = get_template('../templates/emails/confirmation-demande-info-suivi-intensif.html')
    subject, from_email = "Demande d'information - Suivi intensif", 'info@blocusassistance.be'
    to = settings.EMAILS
    d = {'demande':demande}
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    c = {'main_title':'Demande envoyée - Suivi Intensif', 'title': "Nous avons bien reçu votre demande",'texte': "Le responsable pédagogique prendra contact avec vous dans les plus brefs délais"}
    return render(request, "suivi-intensif/confirmation.html", c)
  c = {'form':form}
  return render(request, 'suivi-intensif/inscription.html', c)

