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
from .models import Campus, Universite, Faculte, Etude

########################################
##########                    ##########
##########      GENERAL       ##########
##########                    ##########
########################################
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
  c = {'monprenom':"Pierre"}
  return render(request, 'conditions-generales.html', c)

@minified_response
#@gzip_page
def show_gallerie(request):
  c = {}
  return render(request, 'gallerie.html', c)

@minified_response
#@gzip_page
def contact(request):
  c = {}
  return render(request, 'contact.html', c)

@minified_response
#@gzip_page
def outils_methodes(request):
  c = {}
  return render(request, 'outils-methodes.html', c)

@minified_response
#@gzip_page
def a_propos(request):
  c = {}
  return render(request, 'a-propos.html', c)

########################################
##########                    ##########
##########    ERROR PAGES     ##########
##########                    ##########
########################################
@minified_response
def custom404(request):
    return render(request, '404.html')

@minified_response
def custom500(request):
    return render(request, '500.html')

########################################
##########                    ##########
##########       AJAX         ##########
##########                    ##########
########################################
def ajax_get_facultes(request, pk):
    universite = Universite.objects.get(pk=pk)
    facultes = Faculte.objects.filter(universite = universite)
    facultes_dict=[]
    [facultes_dict.append((faculte.pk,faculte.nom)) for faculte in facultes]
    return HttpResponse(simplejson.dumps(facultes_dict), content_type="application/json")

def ajax_get_etudes(request, pk):
    faculte = Faculte.objects.get(pk=pk)
    etudes = Etude.objects.filter(faculte = faculte)
    etudes_dict=[]
    [etudes_dict.append((etude.pk,etude.nom)) for etude in etudes]
    return HttpResponse(simplejson.dumps(etudes_dict), content_type="application/json")


