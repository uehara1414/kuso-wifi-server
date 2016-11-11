from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ListView.as_view(), name='index'),
    url(r'^honto-kuso/$', views.ajax_post)
]