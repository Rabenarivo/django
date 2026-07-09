from django.db import models


class Medicine_type(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    type = models.ForeignKey(Medicine_type, on_delete=models.CASCADE, related_name='medicines', null=True, blank=True)
    stock_min = models.PositiveIntegerField(default=2)
    price = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    def __str__(self):
        return self.name

class Medicine_stock(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='stock')
    quantity_in_stock = models.PositiveIntegerField(default=0)
    numero_lot = models.CharField(max_length=200)
    expiration_date = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.medicine.name





class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Entrée'),
        ('OUT', 'Sortie'),
        ('ADJ', 'Ajustement'),
    ]

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField()  # Quantity for IN/OUT, absolute value for ADJ
    adjustment_value = models.IntegerField(blank=True, null=True)  # For ADJ: + or - to set new stock
    reference = models.CharField(max_length=200, blank=True, null=True)  # e.g., Prescription #, Sale #, Supplier name
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.movement_type == 'ADJ':
            return f"{self.get_movement_type_display()} - {self.medicine.name} (to {self.adjustment_value})"
        return f"{self.get_movement_type_display()} - {self.medicine.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        # Mettre à jour le stock dans les lots (Medicine_stock)
        if not self.pk:  # Seulement à la création
            if self.movement_type == 'OUT':
                # Logique FIFO : on déduit d'abord des lots qui périment le plus tôt
                remaining = self.quantity
                stocks = self.medicine.stock.filter(quantity_in_stock__gt=0).order_by('expiration_date')
                for stock in stocks:
                    if remaining <= 0:
                        break
                    if stock.quantity_in_stock >= remaining:
                        stock.quantity_in_stock -= remaining
                        stock.save()
                        remaining = 0
                    else:
                        remaining -= stock.quantity_in_stock
                        stock.quantity_in_stock = 0
                        stock.save()
            # Pour 'IN', on ne fait rien car le stock est déjà créé dans Medicine_stock
        super().save(*args, **kwargs)


class Sale(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('COMPLETED', 'Terminée'),
        ('CANCELLED', 'Annulée'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Vente {self.id} - {self.created_at.date()}"

    def calculate_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save()

    def create_stock_movements(self):
        for item in self.items.all():
            # Check if movement already exists
            if not StockMovement.objects.filter(
                medicine=item.medicine,
                reference=f"Vente {self.id}",
                movement_type='OUT'
            ).exists():
                StockMovement.objects.create(
                    medicine=item.medicine,
                    movement_type='OUT',
                    quantity=item.quantity,
                    reference=f"Vente {self.id}"
                )

    def save(self, *args, **kwargs):
        # If status changed to COMPLETED, create stock movements
        if self.pk:
            old_status = Sale.objects.get(pk=self.pk).status
            if old_status != 'COMPLETED' and self.status == 'COMPLETED':
                self.create_stock_movements()
        super().save(*args, **kwargs)


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.medicine.name} - {self.subtotal}"

    def save(self, *args, **kwargs):
        # Calculate subtotal if not set
        if not self.subtotal:
            self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
