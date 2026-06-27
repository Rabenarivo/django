from django.db import models
from appointments.models import Appointment

class Consultation(models.Model):

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE
    )

    diagnosis = models.TextField()

    treatment = models.TextField()

    observation = models.TextField(blank=True)

    consultation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation {self.id}"