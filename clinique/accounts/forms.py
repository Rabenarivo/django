from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from patients.models import Patient


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=Patient.GENDER, required=True)
    phone = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    blood_group = forms.CharField(max_length=5, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                  'birth_date', 'gender', 'phone', 'address', 'blood_group')
