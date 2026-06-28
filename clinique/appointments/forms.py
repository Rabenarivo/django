# d:\ITU\django\clinique\appointments\forms.py
from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'reason']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['status'].initial = 'Pending'
    self.fields['patient'].initial = self.request.user