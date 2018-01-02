from django.conf.urls import include, url
from django.contrib import admin
from blocus.views import inscription_blocus

urlpatterns = [
    url('^inscription$', inscription_blocus, name="inscription_blocus"),
]
