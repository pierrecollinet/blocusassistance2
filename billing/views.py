# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.conf import settings

from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.template import Context

from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.contrib.sitemaps import Sitemap

import json
import json as simplejson

from datetime import datetime, timedelta
from django.views.decorators.gzip import gzip_page

from htmlmin.decorators import minified_response

from django.utils.http import is_safe_url
from .models import BillingProfile, Card

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY")
stripe.api_key = STRIPE_SECRET_KEY

def payment_method_view(request):
    #next_url =
    # if request.user.is_authenticated():
    #     billing_profile = request.user.billingprofile
    #     my_customer_id = billing_profile.customer_id

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("inscription_blocus")
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})

def payment_method_createview(request):
  if request.method == "POST" and request.is_ajax():
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
      return HttpResponse({"message":"Impossible de trouver cet utilisateur"}, status_code=401)
    token = request.POST.get("token")
    if token is not None:
    #  customer = stripe.Customer.retrieve(billing_profile.customer_id)
    #  card_response = customer.sources.create(source=token)
    #  new_card_obj = Card.objects.add_new(billing_profile, token)
      new_card_obj = Card.objects.add_new(billing_profile, token)
      return JsonResponse({"message":"Félicitations ! Votre carte a été ajoutée avec succès."})
  return HttpResponse("error", status=401)












