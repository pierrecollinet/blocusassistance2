from django.conf.urls import include, url
from django.contrib import admin

from suiviintensif.views import accueil

urlpatterns = [
    url('^$', accueil),
    url('^accueil$', accueil, name="accueil-suivi-intensif"),
]
