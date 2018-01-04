from django.conf.urls import include, url
from django.contrib import admin
from fondateurs.views import dashboard

urlpatterns = [
    url('^tableau-de-bord/$', dashboard, name="fondateurs-dashboard"),
]
