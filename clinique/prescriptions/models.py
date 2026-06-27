from django.db import models
from consultations.models import Consultation
from medicines.models import Medicine

class Prescription(models.Model):

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE
    )

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE
    )

    dosage = models.CharField(max_length=100)

    frequency = models.CharField(max_length=100)

    duration = models.CharField(max_length=100)

    def __str__(self):
        return self.medicine.name