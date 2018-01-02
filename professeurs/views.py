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
from professeurs.models import Professeur

#import forms
from professeurs.forms import ProfesseurModelForm


def professeur_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated():
            return decorated_view_func(request)  # return redirect to signin
        if len(Professeur.objects.filter(user=request.user))==1:
            professeur = Professeur.objects.get(user=request.user)
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('completer-profil-prof'))
    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper


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
      return HttpResponseRedirect(reverse('voir-profil-prof', kwargs={'pk':request.user.professeur.pk}))
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
def modify_profile(request):
  form = ProfesseurModelForm(request.POST or None, instance = request.user.professeur)
  if form.is_valid():
    form.save()
    messages.success(request, 'Profil mis à jour')
    return HttpResponseRedirect(reverse('voir-profil-prof', kwargs={'pk':request.user.professeur.pk}))
  c = {'form':form}
  return render(request, 'professeurs/modifier-profil.html', c)

