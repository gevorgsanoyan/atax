from django import forms
from .models import cars, tDriver
from client.models import Gender

class driverForm(forms.ModelForm):
    dDOB = forms.DateField(widget=forms.SelectDateWidget(years=range(1920, 2040)))

    def __init_subclass__(self, *args, **kwargs):
        gt = kwargs.pop('gt', None)
        super(driverForm, self).__init__(*args, **kwargs)
        gdrs = Gender.objects.filter(gType=gt)
        self.fields['gt'].choices = [(g.gType, g.gTypeDescr) for g in gdrs]
        carId = kwargs.pop('carId', None)
        super(driverForm, self).__init__(*args, **kwargs)
        crs = cars.objects.filter(id=carId)
        self.fields['carId'].choices = [(cr.id, str(cr.cMake) + " " + cr.cModel + " " + str(cr.pYear) + " " + str(cr.cColor)) for cr in crs]

    class Meta:
        model = tDriver
        fields = ('dFirstName', 'dLastName', 'dDocNumber', 'dDOB', 'dGender', 'dEmail', 'dPhone', 'dTlgMsg', 'dCar', 'isReviewed', 'isActive', 'dCarInfo')

        labels = {
            'dFirstName': ('First name:'),
            'dLastName': ('Last name:'),
            'dDocNumber': ('Doc.numb.:'),
            'dDOB': ('DOB:'),
            'dGender': ('Gender:'),
            'dEmail': ('Email:'),
            'dPhone': ('Phone'),
            'dTlgMsg': ('Telegram'),
            'dCar': ('Car'),
            'isReviewed': ('Is reviewed'),
            'isActive': ('Active'),
            'dCarInfo': ('Info about car from driver')
        }