from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^response/$', views.chat_index, name='chat_response'),
]
