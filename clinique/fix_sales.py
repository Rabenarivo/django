import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinique.settings")
django.setup()

from medicines.models import Sale, SaleItem, Medicine
from prescriptions.models import Prescription, PrescriptionItem

try:
    sale = Sale.objects.get(id=5)
    if not sale.items.exists():
        # Get the medicine from Prescription 9 or just Paracetamol
        prescription = Prescription.objects.get(id=9)
        for p_item in prescription.items.all():
            SaleItem.objects.get_or_create(
                sale=sale,
                medicine=p_item.medicine,
                defaults={
                    'quantity': p_item.quantity,
                    'unit_price': p_item.medicine.price,
                    'subtotal': p_item.quantity * p_item.medicine.price
                }
            )
        sale.calculate_total()
        print("Fixed Sale 5 with items from Prescription 9")
    else:
        print("Sale 5 already has items.")
except Exception as e:
    print("Error:", e)
