from django.conf.urls import include, url
from django.contrib import admin
from blocus.views import inscription_blocus, blocus_assistes

urlpatterns = [
    url('^$', blocus_assistes, name="blocus-assistes"),
    url('^accueil$', blocus_assistes, name="blocus-assistes"),
    url('^inscription$', inscription_blocus, name="inscription_blocus"),
]
