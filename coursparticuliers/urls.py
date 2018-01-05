from django.conf.urls import include, url
from django.contrib import admin

from coursparticuliers.views import accueil

urlpatterns = [
    url('^$', accueil),
    url('^accueil$', accueil, name="accueil-cours-particuliers"),
]
