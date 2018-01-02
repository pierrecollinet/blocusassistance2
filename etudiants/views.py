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

# import models
#from .models import Campus
from etudiants.models import Etudiant

#import forms
from etudiants.forms import EtudiantModelForm

@login_required
@minified_response
#@gzip_page
def modify_profile(request):
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
      user.save
      return HttpResponseRedirect(reverse('inscription_blocus'))
    c = {'form':form}
    return render(request, 'modifier-profil.html', c)
  else :
    return HttpResponseRedirect(reverse('inscription_blocus'))

