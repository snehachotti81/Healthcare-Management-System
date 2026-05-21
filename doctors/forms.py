from doctors.models import Appointment
from django import forms


class AppointmentForm(forms.ModelForm):
    consultation_charges = forms.CharField(disabled=True, required=False)

    class Meta:
        model = Appointment
        fields = ['consultation_charges', 'patient_name', 'gender',
                  'patient_email', 'patient_phone', 'doctorname',
                  'date', 'time', 'reason']
        widgets = {
            'consultation_charges': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'patient_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'patient_phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
            'doctorname': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for visit (optional)'}),
        }