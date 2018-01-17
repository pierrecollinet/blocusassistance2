from django.conf.urls import include, url
from django.contrib import admin

from suiviintensif.views import accueil, inscription_suiviintensif

urlpatterns = [
    url('^$', accueil),
    url('^accueil$', accueil, name="accueil-suivi-intensif"),
    url('^inscription$', inscription_suiviintensif, name="inscription-suivi-intensif"),
]
