from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^honto-kuso/$', views.ajax_post),
    url(r'^(?P<year>[0-9]+)年(?P<month>[0-9]+)月(?P<day>[0-9]+)日にどれだけクソだったか$', views.one_day_view, name="one_day_kuso"),
    url(r'^timeline_ajax', views.timeline_ajax, name='timeline_ajax'),
    url(r'^ajax-filter$', views.post_filter_settings, name='ajax-filter'),
    url(r'^ssid-ajax$', views.ssid_ajax, name='ssid-ajax'),
]