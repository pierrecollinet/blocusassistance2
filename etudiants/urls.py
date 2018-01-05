from django.conf.urls import include, url
from django.contrib import admin
from etudiants.views import modify_profile, complete_profile, show_profile, dashboard

urlpatterns = [
    url('^completer-profil/$', complete_profile, name="completer-profil-etudiants"),
    url('^modifier-profil/$', modify_profile, name="modifier-profil-etudiants"),
    url('^profil/(?P<pk>\d+)$', show_profile, name="voir-profil-etudiants"),
    url('^tableau-de-bord$', dashboard, name="tableau-de-bord-etudiants"),
]
