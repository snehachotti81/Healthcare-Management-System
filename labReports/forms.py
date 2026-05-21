from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from labReports.models import Lab_Tests


class LabTechRegistrationForm(UserCreationForm):
    emp_id        = forms.IntegerField()
    Qualification = forms.CharField(max_length=100)
    year_of_exp   = forms.IntegerField()
    address       = forms.CharField(max_length=200)

    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2',
                  'emp_id', 'Qualification', 'year_of_exp', 'address']
        

class LabTestForm(forms.ModelForm):
    class Meta:
        model = Lab_Tests
        fields = "__all__"        