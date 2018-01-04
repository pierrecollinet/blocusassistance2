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

# import models
from .models import Campus

@minified_response
#@gzip_page
def welcome(request):
  c = {'campus': Campus.objects.all()}
  return render(request, 'welcome.html', c)

@minified_response
#@gzip_page
def politique_confidentialite(request):
  c = {}
  return render(request, 'politique-confidentialite.html', c)

@minified_response
#@gzip_page
def conditions_generales(request):
  c = {}
  return render(request, 'conditions-generales.html', c)
