from django import forms
from django.contrib.auth.models import User
from .models import Patient, MedicalProfile

class PatientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer pour n'afficher que les utilisateurs ayant le rôle 'CLIENT'
        self.fields['user'].queryset = User.objects.filter(profile__role='CLIENT')

    class Meta:
        model = Patient
        fields = ['user', 'first_name', 'last_name', 'birth_date', 'gender', 'phone', 'email', 'address', 'blood_group']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'blood_group': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MedicalProfileForm(forms.ModelForm):
    class Meta:
        model = MedicalProfile
        fields = ['medical_history', 'surgical_history', 'family_history', 'allergies', 'risk_factors']
        widgets = {
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'surgical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'family_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'risk_factors': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
