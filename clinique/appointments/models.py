from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):

    STATUS = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True) 

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.appointment_date}"