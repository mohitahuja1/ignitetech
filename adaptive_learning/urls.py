from django.conf.urls import include, url
from . import views


urlpatterns = [

    url(r'^$', views.index, name='index'),

    url(r'^(?P<questionid>[0-9]+)/$', views.details, name='details'),

    url(r'^(?P<questionid>[0-9]+)/check/$', views.check, name='check'),

    url(r'^result/', views.result, name='result')

]
