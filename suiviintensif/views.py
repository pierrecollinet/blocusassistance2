# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context

from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required

from django.contrib.sitemaps import Sitemap

import json
from datetime import datetime, timedelta
from django.views.decorators.gzip import gzip_page

from htmlmin.decorators import minified_response

from blocus.forms import InscriptionBlocusModelForm


@minified_response
#@gzip_page
def accueil(request):
  c = {}
  return render(request, 'suivi-intensif/accueil.html', c)

@minified_response
#@gzip_page
def inscription_suiviintensif(request):
  form = InscriptionBlocusModelForm(request.POST or None)
  if form.is_valid():
    "do something"
  c = {'form':form}
  return render(request, 'suivi-intensif/inscription.html', c)

