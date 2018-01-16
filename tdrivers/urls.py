from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^tdrivers$', views.driversList, name='driverslist'),
    url(r'^tdrivers/new$', views.driverInput, name='driverinput'),
    url(r'^tdrivers/edit/(?P<driverId>\d+)/$', views.driverEdit, name='driveredit'),
]