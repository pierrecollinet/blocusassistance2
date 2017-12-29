from django.conf.urls import include, url
from django.contrib import admin

from ba2.views import welcome

urlpatterns = [
    url('^$', welcome),
    url('^welcome$', welcome, name="welcome"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('wordpress_api.urls')),

    # internal apps
    url(r'^blocus-assistes/', include('blocus.urls')),
]
