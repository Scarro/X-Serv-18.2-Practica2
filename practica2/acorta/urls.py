from django.conf.urls import url
from . import views

app_name = 'acortadora'
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<acortada>[0-9]+)/$', views.redirigir, name='redirigir'),
]