from django import forms
from .models import Prescription, PrescriptionItem
from consultations.models import Consultation


class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptionItem
        fields = ['medicine', 'dosage', 'frequency', 'duration']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'medicine-select'}),
            'dosage': forms.TextInput(attrs={'class': 'dosage-input', 'placeholder': 'Dosage'}),
            'frequency': forms.TextInput(attrs={'class': 'frequency-input', 'placeholder': 'Fréquence'}),
            'duration': forms.TextInput(attrs={'class': 'duration-input', 'placeholder': 'Durée'}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['consultation']
