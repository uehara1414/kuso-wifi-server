from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ListView.as_view(), name='index'),
    url(r'^kuso-wifi-post/$', views.ajax_post)
]