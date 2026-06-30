from django import forms
from .models import Medicine, StockMovement, Sale

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'price']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['patient', 'total_amount', 'status']

class SaleStatusForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['status']
