from django.db import models


class Medicine(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    dosage_form = models.CharField(max_length=100, blank=True, null=True)
    strength = models.CharField(max_length=100, blank=True, null=True)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expiration_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


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
        # Update medicine stock when saving movement
        if not self.pk:  # Only if new movement
            if self.movement_type == 'IN':
                self.medicine.quantity_in_stock += self.quantity
            elif self.movement_type == 'OUT':
                self.medicine.quantity_in_stock -= self.quantity
            elif self.movement_type == 'ADJ' and self.adjustment_value is not None:
                self.medicine.quantity_in_stock = self.adjustment_value
        self.medicine.save()
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
