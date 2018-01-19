from django.conf.urls import include, url
from django.contrib import admin

from coursparticuliers.views import accueil, inscription_cp
from ba2.views import success

urlpatterns = [
    url('^$', accueil),
    url('^accueil$', accueil, name="accueil-cours-particuliers"),
    url('^inscription$', inscription_cp, name="inscription-cours-particuliers"),
    url('^confirmation-demande-cours$', success, name="confirmation-demande-cours"),
]
