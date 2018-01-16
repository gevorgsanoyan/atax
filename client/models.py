from django.db import models
from django.utils import timezone
#from tdrivers.models import tDriver


class Gender(models.Model):
    gType = models.CharField(max_length=2)
    gTypeDescr = models.CharField(max_length=20)

    def __str__(self):
        return self.gType


# Create your models here.
class Client(models.Model):
    cFirstName = models.CharField(max_length=200)
    cLastName = models.CharField(max_length=200)
    cDocNumber = models.CharField(max_length=50)
    cDOB = models.DateField(null=True, blank=True)
    cGender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    cEmail = models.EmailField(null=True, blank=True)
    cPhone = models.CharField(max_length=20, null=True, blank=True)
    cTlgMsg = models.CharField(max_length=20, null=True, blank=True)

    iUser = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.cFirstName + " " + self.cLastName + " " + self.cDocNumber


class Airports(models.Model):
    apName = models.CharField(max_length=100)
    apCity =  models.CharField(max_length=100)
    apShortName = models.CharField(max_length=50)

    def __str__(self):
        return self.apName + " (" + self.apCity + ")"


class Destination(models.Model):
    dName = models.CharField(max_length=100)
    dCity = models.CharField(max_length=100)
    dAddress = models.CharField(max_length=100)

    def __str__(self):
        return self.dName


class ClientFlight(models.Model):
    fClient = models.ForeignKey(Client, on_delete=models.CASCADE)
    fAirport = models.ForeignKey(Airports, on_delete=models.CASCADE)
    flNumber = models.CharField(max_length=50)
    flDate = models.DateTimeField()
    flDestination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    flDestOther = models.CharField(max_length=1000)
    isAnnounced = models.BooleanField(default=False)
    isAccepted = models.BooleanField(default=False, blank=True)
    accDate = models.DateTimeField(default=timezone.now, null=True, blank=True)
    accpDriver = models.ForeignKey('tdrivers.tDriver', on_delete=models.CASCADE)

    def __str__(self):
        return self.flNumber + " " + str(self.flDate)
