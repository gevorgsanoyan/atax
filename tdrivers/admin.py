from django.contrib import admin
from .models import carMake, cars, cColors, tDriver
# Register your models here.
admin.site.register(carMake)
admin.site.register(cars)
admin.site.register(cColors)
admin.site.register(tDriver)
