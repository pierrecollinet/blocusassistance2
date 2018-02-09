# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
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
from django.contrib import messages

# import models
#from .models import Campus
from etudiants.models import Etudiant

#import forms
from etudiants.forms import EtudiantModelForm, EtudiantFullModelForm


def etudiant_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated():
            return decorated_view_func(request)  # return redirect to signin
        if len(Etudiant.objects.filter(user=request.user, active=True))==1:
            etudiant = Etudiant.objects.get(user=request.user)
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('completer-profil-etudiants'))
    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper

@etudiant_required
@minified_response
#@gzip_page
def dashboard(request):#, pk):
#  student = Etudiant.objects.get(pk=pk)
  c = {}#'student':student}
  return render(request, 'tableau-de-bord.html', c)

@minified_response
#@gzip_page
def complete_profile(request):
  if request.GET and 'next' in request.GET :
    next_url = request.GET.get("next","")
  else :
    next_url = ""
  if len(Etudiant.objects.filter(user=request.user)) == 0 :
    form = EtudiantModelForm(request.POST or None)
    if form.is_valid():
      # On sauve un nouvel étudiant
      etudiant = form.save(commit=False)
      user = request.user
      etudiant.user = user
      etudiant.save()

      # On update les infos de ce user
      user.first_name = etudiant.prenom
      user.last_name = etudiant.nom
      user.email = etudiant.email
      user.save()
      if request.POST and 'next_url' in request.POST and request.POST["next_url"] != "":
        return HttpResponseRedirect(request.POST["next_url"])
      return HttpResponseRedirect(reverse('inscription_blocus'))
    c = {'form':form, 'next_url':next_url}
    return render(request, 'completer-profil.html', c)
  else :
    return HttpResponseRedirect(reverse('inscription_blocus'))

@etudiant_required
@minified_response
#@gzip_page
def show_profile(request, pk):
  student = Etudiant.objects.get(pk=pk)
  c = {'student':student}
  return render(request, 'voir-profil.html', c)

@etudiant_required
@minified_response
#@gzip_page
def modify_profile(request):
  form = EtudiantFullModelForm(request.POST or None, instance = request.user.etudiant)
  if form.is_valid():
    form.save()
    messages.success(request, 'Profil mis à jour')
    return HttpResponseRedirect(reverse('voir-profil', kwargs={'pk':request.user.etudiant.pk}))
  c = {'form':form}
  return render(request, 'modifier-profil.html', c)

