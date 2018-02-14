from django.conf.urls import include, url
from django.contrib import admin
from professeurs.views import modify_profile, complete_profile, show_profile, accueil, dashboard, show_student, complete_profile_student, encoder_journee_blocus,modifier_journee_blocus,supprimer_journee_blocus, suivi_journalier_blocus,voir_suivi_journalier,modifier_suivi_journalier, display_rapport_journalier, send_rapport_journalier
from professeurs.views import send_rapport_module, display_rapport_module
urlpatterns = [
    # PROFIL PROFESSEURS
    url('^completer-profil/$', complete_profile, name="completer-profil-prof"),
    url('^modifier-profil/$', modify_profile, name="modifier-profil-prof"),
    url('^profil/(?P<pk>\d+)$', show_profile, name="voir-profil-prof"),
    url('^voir-profil-etudiant/(?P<pk>\d+)$', show_student, name="voir-profil-etudiant-for-prof"),
    url('^completer-profil-etudiant/(?P<pk>\d+)$', complete_profile_student, name="completer-profil-etudiant-for-prof"),
    url('^$', accueil, name="accueil-prof"),
    url('^accueil$', accueil, name="accueil-prof"),
    url('^tableau-de-bord$', dashboard, name="tableau-de-bord-professeurs"),

    # JOURNEE BLOCUS PROFESSEUR
    url('^encoder-journee-blocus$', encoder_journee_blocus, name="encoder-journee-blocus"),
    url('^modifier-journee-blocus/(?P<pk>\d+)$', modifier_journee_blocus, name="modifier-journee-blocus"),
    url('^supprimer-journee-blocus/(?P<pk>\d+)$', supprimer_journee_blocus, name="supprimer-journee-blocus"),

    # RAPPORTS DE BLOCUS
    url('^suivi-journalier-blocus/(?P<pk>\d+)$', suivi_journalier_blocus, name="suivi-journalier-blocus"),
    url('^voir-suivi-journalier/(?P<pk>\d+)$', voir_suivi_journalier, name="voir-suivi-journalier"),
    url('^modifier-suivi-journalier/(?P<pk>\d+)$', modifier_suivi_journalier, name="modifier-suivi-journalier"),
    # PDF
    url('^display-rapport-journalier/(?P<pk>\d+)$', display_rapport_journalier, name="display-rapport-journalier"),
    url('^send-rapport-journalier/(?P<pk>\d+)$', send_rapport_journalier, name="send-rapport-journalier"),
    url('^display-rapport-module/(?P<pk_etudiant>\d+)/(?P<pk_module>\d+)$', display_rapport_module, name="display-rapport-module"),
    url('^send-rapport-module/(?P<pk_etudiant>\d+)/(?P<pk_module>\d+)$', send_rapport_module, name="send-rapport-module"),

]
