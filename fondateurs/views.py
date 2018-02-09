# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.urls import reverse

from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.sitemaps import Sitemap

import json
import json as simplejson

from datetime import datetime, timedelta
from django.views.decorators.gzip import gzip_page

from htmlmin.decorators import minified_response

# import models
from ba2.models import Campus, Universite, Faculte, Etude
from blocus.models import Blocus

def fondateur_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated():
            return decorated_view_func(request)  # return redirect to signin
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            # redirect vers une page demandant de contacter un admin pour devenir actif
            return HttpResponseRedirect(reverse('welcome'))
    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper


@fondateur_required
@minified_response
#@gzip_page
def dashboard(request):
  blocus = Blocus.objects.all()
  c = {'blocus':blocus}
  return render(request, 'fondateurs/dashboard.html', c)

@fondateur_required
@minified_response
#@gzip_page
def summary_blocus(request,pk):
  blocus = Blocus.objects.get(pk=pk)
  c = {'blocus':blocus}
  return render(request, 'fondateurs/blocus-assistes/summary-blocus.html',c)




