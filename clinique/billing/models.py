from django.db import models
from consultations.models import Consultation


class Invoice(models.Model):

    STATUS_CHOICES = [
        ('UNPAID', 'Non payé'),
        ('PAID', 'Payé'),
        ('PARTIAL', 'Partiellement payé'),
    ]

    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='UNPAID'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Facture #{self.id}"