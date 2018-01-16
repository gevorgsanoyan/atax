from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^client$', views.clientsList, name='clientslist'),
    url(r'^client/new$', views.clientInput, name='clientinput'),
    url(r'^client/edit/(?P<clientId>\d+)/$', views.clientEdit, name='clientedit'),
    url(r'^client/flights/(?P<crId>(\d+))/$', views.flightsList, name='flightslist'),
    url(r'^client/flights/announce$', views.flightAnnounce, name='flightannounce'),
]