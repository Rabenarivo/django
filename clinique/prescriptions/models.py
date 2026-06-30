from django.db import models
from consultations.models import Consultation
from medicines.models import Medicine


class Prescription(models.Model):
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription {self.id} - {self.consultation.appointment.patient.first_name}"

from django.db import models
from consultations.models import Consultation
from medicines.models import Medicine


class Prescription(models.Model):
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription {self.id} - {self.consultation.appointment.patient.first_name}"


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, related_name='items', on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.quantity}x {self.medicine.name} - {self.dosage}"