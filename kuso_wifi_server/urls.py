from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^honto-kuso/$', views.ajax_post),
    url(r'^(?P<year>[0-9]+)年(?P<month>[0-9]+)月(?P<day>[0-9]+)日にどれだけクソだったか$', views.one_day_view, name="one_day_kuso"),
]