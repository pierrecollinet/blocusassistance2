from django.conf.urls import include, url
from django.contrib import admin
from blocus.views import inscription_blocus, blocus_assistes, confirmation_inscription, ajax_get_modules, ajax_calculate_price, checkout

urlpatterns = [
    url('^$', blocus_assistes, name="blocus-assistes"),
    url('^accueil$', blocus_assistes, name="blocus-assistes"),
    url('^inscription$', inscription_blocus, name="inscription_blocus"),
    url('^checkout/(?P<pk>\d+)$', checkout, name="checkout"),
    url('^confirmation-inscription$', confirmation_inscription, name="confirmation-inscription-blocus"),

    # Ajax
    url('^get_modules/(?P<pk>\d+)/$', ajax_get_modules),
    url('^calculate_price_ajax/$', ajax_calculate_price),
]
