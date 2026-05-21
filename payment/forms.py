from django import forms
from .models import DischargeSummary, Payment


class DischargeSummaryForm(forms.ModelForm):
    class Meta:
        model  = DischargeSummary
        fields = [
            'patient_name', 'doctor', 'treatment', 'description',
            'doa', 'dod', 'room_type', 'total_days',
            'food_morning', 'food_lunch', 'food_dinner', 'food_coffee_tea',
        ]
        widgets = {
            'doa':          forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dod':          forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description':  forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'patient_name': forms.Select(attrs={'class': 'form-select'}),
            'doctor':       forms.Select(attrs={'class': 'form-select'}),
            'room_type':    forms.Select(attrs={'class': 'form-select'}),
            'treatment':    forms.TextInput(attrs={'class': 'form-control'}),
            'total_days':   forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'doa':           'Date of Admission (DOA)',
            'dod':           'Date of Discharge (DOD)',
            'food_morning':    'Morning (₹120/day)',
            'food_lunch':      'Lunch (₹200/day)',
            'food_dinner':     'Dinner (₹160/day)',
            'food_coffee_tea': 'Coffee/Tea (₹40/day)',
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model  = Payment
        fields = ['payment_method', 'transaction_id']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'transaction_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter transaction ID (optional for cash)'
            }),
        }
        labels = {
            'payment_method': 'Payment Method',
            'transaction_id': 'Transaction ID',
        }