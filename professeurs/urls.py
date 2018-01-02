from django.conf.urls import include, url
from django.contrib import admin
from professeurs.views import modify_profile, complete_profile, show_profile

urlpatterns = [
    url('^completer-profil/$', complete_profile, name="completer-profil-prof"),
    url('^modifier-profil/$', modify_profile, name="modifier-profil-prof"),
    url('^profil/(?P<pk>\d+)$', show_profile, name="voir-profil-prof"),
]
