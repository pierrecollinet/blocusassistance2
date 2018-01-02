from django.conf.urls import include, url
from django.contrib import admin
from etudiants.views import modify_profile, complete_profile, show_profile

urlpatterns = [
    url('^completer-profil/etudiant/$', complete_profile, name="completer-profil"),
    url('^modifier-profil/$', modify_profile, name="modifier-profil"),
    url('^profil/(?P<pk>\d+)$', show_profile, name="voir-profil"),
]
