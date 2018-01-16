from django.contrib import admin
from .models import Gender
from .models import Client
from .models import Airports
from .models import Destination
from .models import ClientFlight

# Register your models here.
admin.site.register(Gender)
admin.site.register(Client)
admin.site.register(Airports)
admin.site.register(Destination)
admin.site.register(ClientFlight)