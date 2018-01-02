from django.conf.urls import include, url
from django.contrib import admin
from etudiants.views import modify_profile

urlpatterns = [
    url('^completer-profil/etudiant/$', modify_profile, name="completer-profil"),
]
