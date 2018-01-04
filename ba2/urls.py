from django.conf.urls import include, url
from django.contrib import admin

from ba2.views import welcome, politique_confidentialite, conditions_generales, ajax_get_facultes, ajax_get_etudes

urlpatterns = [
    url('^$', welcome),
    url('^welcome$', welcome, name="welcome"),
    url('^politique-confidentialite$', politique_confidentialite, name="politique-confidentialite"),
    url('^conditions-generales$', conditions_generales, name="conditions-generales"),
    url('^get_facultes/(?P<pk>\d+)/$', ajax_get_facultes),
    url('^get_etudes/(?P<pk>\d+)/$', ajax_get_etudes),

    # not working for the moment
    url(r'^blog/', include('wordpress_api.urls')),

    # internal apps
    url(r'^blocus-assistes/', include('blocus.urls')),
    url(r'^etudiants/', include('etudiants.urls')),
    url(r'^professeurs/', include('professeurs.urls')),
    url(r'^fondateurs/', include('fondateurs.urls')),

    # external apps
    url(r'^accounts/', include('allauth.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),
]

from ba2.views import custom404, custom500
handler404 = custom404
handler500 = custom500
