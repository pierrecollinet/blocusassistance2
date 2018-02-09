from django.conf.urls import include, url
from django.contrib import admin
from professeurs.views import modify_profile, complete_profile, show_profile, accueil, dashboard, show_student, complete_profile_student

urlpatterns = [
    url('^completer-profil/$', complete_profile, name="completer-profil-prof"),
    url('^modifier-profil/$', modify_profile, name="modifier-profil-prof"),
    url('^profil/(?P<pk>\d+)$', show_profile, name="voir-profil-prof"),
    url('^voir-profil-etudiant/(?P<pk>\d+)$', show_student, name="voir-profil-etudiant-for-prof"),
    url('^completer-profil-etudiant/(?P<pk>\d+)$', complete_profile_student, name="completer-profil-etudiant-for-prof"),
    url('^$', accueil, name="accueil-prof"),
    url('^accueil$', accueil, name="accueil-prof"),
    url('^tableau-de-bord$', dashboard, name="tableau-de-bord-professeurs"),
]
