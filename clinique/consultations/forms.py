from django import forms
from .models import Consultation


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['appointment', 'diagnosis', 'treatment', 'observation']
        widgets = {
            'appointment': forms.Select(attrs={'class': 'form-select', 'readonly': 'readonly'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Saisissez le diagnostic...'}),
            'treatment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Saisissez le traitement...'}),
            'observation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Saisissez vos observations complémentaires...'}),
        }
