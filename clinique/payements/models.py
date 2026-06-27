from django.db import models
from billing.models import Invoice


class Payment(models.Model):

    METHOD_CHOICES = [
        ('CASH', 'Espèces'),
        ('CARD', 'Carte bancaire'),
        ('MOBILE', 'Mobile Money'),
    ]

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Paiement {self.invoice.id}"