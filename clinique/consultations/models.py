from django.db import models
from appointments.models import Appointment
from patients.models import Patient

class Consultation(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    observation = models.TextField(blank=True)
    consultation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation {self.id} - {self.appointment.patient.first_name}"

class VitalSign(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vital_signs')
    consultation = models.OneToOneField(Consultation, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Constantes
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Poids en kg")
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Taille en cm")
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Température en °C")
    blood_pressure_systolic = models.IntegerField(blank=True, null=True, help_text="Pression systolique (ex: 120)")
    blood_pressure_diastolic = models.IntegerField(blank=True, null=True, help_text="Pression diastolique (ex: 80)")
    heart_rate = models.IntegerField(blank=True, null=True, help_text="BPM (battements par minute)")
    oxygen_saturation = models.IntegerField(blank=True, null=True, help_text="SpO2 en %")
    
    measured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Constantes de {self.patient} le {self.measured_at.strftime('%d/%m/%Y')}"
