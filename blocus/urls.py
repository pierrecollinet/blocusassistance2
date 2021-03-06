from django.conf.urls import include, url
from django.contrib import admin
from blocus.views import inscription_blocus, blocus_assistes, confirmation_inscription, ajax_get_modules, ajax_calculate_price, checkout, detail_blocus, imprimer_planning, cocher_presence, detail_presence, grille_suivi_etudiants, display_list_student
from blocus.views import ajout_etudiant, ajax_get_students_list, enquete_satisfaction_blocus

urlpatterns = [
    url('^$', blocus_assistes, name="blocus-assistes"),
    url('^accueil$', blocus_assistes, name="blocus-assistes"),
    url('^inscription$', inscription_blocus, name="inscription_blocus"),
    url('^checkout/(?P<pk>\d+)$', checkout, name="checkout"),
    url('^detail-blocus/(?P<pk>\d+)$', detail_blocus, name="detail-blocus"),
    url('^confirmation-inscription$', confirmation_inscription, name="confirmation-inscription-blocus"),

    url('^imprimer-planning/(?P<pk_campus>\d+)/(?P<pk_module>\d+)$', imprimer_planning, name="imprimer-planning"),
    url('^cocher-presence/(?P<pk_campus>\d+)/(?P<pk_module>\d+)$', cocher_presence, name="cocher-presence"),
    url('^liste-etudiants/(?P<pk_campus>\d+)/(?P<pk_module>\d+)$', display_list_student, name="display-list-student"),
    url('^enquete-satisfaction/(?P<pk_campus>\d+)/(?P<pk_module>\d+)$', enquete_satisfaction_blocus, name="enquete-satisfaction-blocus"),
    url('^grille-suivi-etudiants/(?P<pk_campus>\d+)/(?P<pk_module>\d+)$', grille_suivi_etudiants, name="grille-suivi-etudiants"),
    url('^detail-presence/(?P<pk>\d+)/(?P<pk_module>\d+)$', detail_presence, name="detail-presence"),
    url('^ajouter-etudiant-blocus$', ajout_etudiant, name="ajouter-etudiant-blocus"),

    # Ajax
    url('^get_modules/(?P<pk>\d+)/$', ajax_get_modules),
    url('^calculate_price_ajax/$', ajax_calculate_price),
    url('^get_students_list/(?P<string>[\w\-]+)/$', ajax_get_students_list)

]
