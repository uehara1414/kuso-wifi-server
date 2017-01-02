from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('kuso_wifi_server.urls', namespace='kuso_wifi_server')),
    # url(r'^', include('docker_django.apps.kuso_wifi_server')),
]
