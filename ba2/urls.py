from django.conf.urls import include, url
from django.contrib import admin

from ba2.views import welcome, politique_confidentialite, conditions_generales, ajax_get_facultes, ajax_get_etudes, show_gallerie, contact, a_propos, outils_methodes

urlpatterns = [
    url('^$', welcome),
    url('^welcome$', welcome, name="welcome"),
    url('^politique-confidentialite$', politique_confidentialite, name="politique-confidentialite"),
    url('^conditions-generales$', conditions_generales, name="conditions-generales"),
    url('^gallerie$', show_gallerie, name="gallerie"),
    url('^contact$', contact, name="contact"),
    url('^a-propos$', a_propos, name="a-propos"),
    url('^outils-et-methodes$', outils_methodes, name="outils-methodes"),

    # Ajax
    url('^get_facultes/(?P<pk>\d+)/$', ajax_get_facultes),
    url('^get_etudes/(?P<pk>\d+)/$', ajax_get_etudes),

    # not working for the moment
    url(r'^blog/', include('wordpress_api.urls')),

    # internal apps
    url(r'^blocus-assistes/', include('blocus.urls')),
    url(r'^etudiants/', include('etudiants.urls')),
    url(r'^professeurs/', include('professeurs.urls')),
    url(r'^fondateurs/', include('fondateurs.urls')),
    url(r'^suivi-intensif/', include('suiviintensif.urls')),
    url(r'^cours-particuliers/', include('coursparticuliers.urls')),
    url(r'^billing/', include('billing.urls')),

    # external apps
    url(r'^accounts/', include('allauth.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),
]

from ba2.views import custom404, custom500
handler404 = custom404
handler500 = custom500


from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
