from django.db import models
#from client.models import Gender
# Create your models here.

class cColors(models.Model):
    colorName = models.CharField(max_length=50)
    colorValue = models.IntegerField()

    def __str__(self):
        return self.colorName


class carMake(models.Model):
    Make = models.CharField(max_length=50)

    def __str__(self):
        return self.Make


class cars(models.Model):
    cMake = models.ForeignKey(carMake, on_delete=models.CASCADE)
    cModel = models.CharField(max_length=50)
    pYear = models.IntegerField(null=True, blank=True)
    cColor = models.ForeignKey(cColors, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.cMake) + " " + self.cModel


class tDriver(models.Model):
    dFirstName = models.CharField(max_length=200)
    dLastName = models.CharField(max_length=200)
    dDocNumber = models.CharField(max_length=50)
    dDOB = models.DateField(null=True, blank=True)
    dGender = models.ForeignKey('client.Gender', on_delete=models.CASCADE, null=True, blank=True)
    dEmail = models.EmailField(null=True, blank=True)
    dPhone = models.CharField(max_length=20, null=True, blank=True)
    dTlgMsg = models.CharField(max_length=20, null=True, blank=True)

    dCar = models.ForeignKey(cars, on_delete=models.CASCADE, null=True, blank=True)

    dCarInfo = models.CharField(max_length=500, null=True, blank=True)

    isReviewed = models.BooleanField(default=False)
    isActive = models.BooleanField(default=False)

    iUser = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.dFirstName + " " + self.dLastName + ", " + str(self.dCar)

