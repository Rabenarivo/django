from django import forms
from .models import Medicine, StockMovement, Sale , Medicine_stock, Medicine_type

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'price', 'stock_min', 'type', 'description']

class Medicine_stockForm(forms.ModelForm):
    class Meta:
        model = Medicine_stock
        fields = ['medicine', 'quantity_in_stock', 'numero_lot', 'expiration_date']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['patient', 'total_amount', 'status']

class SaleStatusForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['status']

