from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^kuso/', include('docker_django.apps.kuso_wifi_server.urls')),
    # url(r'^', include('docker_django.apps.kuso_wifi_server')),
]
