from django import forms
from .models import Client, Gender, ClientFlight

from datetime import date



class clientForm(forms.ModelForm):
    cDOB = forms.DateField(widget = forms.SelectDateWidget(years=range(1920, 2040)))

    def __init_subclass__(self, *args, **kwargs):
        gt = kwargs.pop('gt', None)
        super(clientForm, self).__init__(*args, **kwargs)
        gdrs = Gender.objects.filter(gType=gt)
        self.fields['gt'].choices = [(g.gType, g.gTypeDescr) for g in gdrs]

    class Meta:
        model = Client
        fields = ('cFirstName', 'cLastName','cDocNumber', 'cDOB', 'cGender', 'cEmail','cPhone')

        labels = {
            'cFirstName': ('First name:'),
            'cLastName': ('Last name:'),
            'cDocNumber': ('Doc.numb.:'),
            'cDOB': ('DOB:'),
            'cGender': ('Gender:'),
            'cEmail': ('Email:'),
            'cPhone': ('Phone')
        }



class flightForm(forms.ModelForm):

    flDate = forms.DateField(widget=forms.SelectDateWidget(years=range(2018, 2040)))

    class Meta:
        model = ClientFlight
        fields = ('fClient', 'fAirport', 'flNumber', 'flDate', 'flDestination', 'flDestOther', 'isAnnounced',
                  'isAccepted', 'accDate', 'accpDriver')
        labels = {
            'fClient':('Client:'),
            'fAirport': ('Airport:'),
            'flNumber': ('Flight numb.:'),
            'flDate': ('Flight date:'),
            'flDestination': ('Destination:'),
            'flDestOther': ('Destination provided by client:'),
            'isAnnounced': ('Driver announcation:'),
            'isAccepted': ('Acception by driver:'),
            'accDate': ('Acception date:'),
            'accpDriver': ('Driver:')
        }