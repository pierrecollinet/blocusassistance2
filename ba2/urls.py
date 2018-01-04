from django.conf.urls import include, url
from django.contrib import admin

from ba2.views import welcome, politique_confidentialite, conditions_generales

urlpatterns = [
    url('^$', welcome),
    url('^welcome$', welcome, name="welcome"),
    url('^politique-confidentialite$', politique_confidentialite, name="politique-confidentialite"),
    url('^conditions-generales$', conditions_generales, name="conditions-generales"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('wordpress_api.urls')),

    # internal apps
    url(r'^blocus-assistes/', include('blocus.urls')),
    url(r'^etudiants/', include('etudiants.urls')),
    url(r'^professeurs/', include('professeurs.urls')),

    # external apps
    url(r'^accounts/', include('allauth.urls')),
]
