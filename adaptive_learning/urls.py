from django.conf.urls import include, url
from . import views


urlpatterns = [

    url(r'^$', views.index, name='index'),

    url(r'^(?P<questionid>[0-9]+)/$', views.details, name='details')

]
