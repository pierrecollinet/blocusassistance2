from django.conf.urls import include, url
from django.contrib import admin
from fondateurs.views import dashboard, summary_blocus

urlpatterns = [
    url('^tableau-de-bord/$', dashboard, name="fondateurs-dashboard"),
    url('^blocus-assistes/(?P<pk>\d+)/$', summary_blocus, name="blocus-assistes-summary"),
]
