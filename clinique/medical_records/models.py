# pyrefly: ignore [missing-import]
from django.db import models
from patients.models import Patient

class MedicalRecord(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='medical_record')
    blood_group = models.CharField(max_length=5, blank=True, null=True) # Ex: A+, O-
    chronic_diseases = models.TextField(blank=True, help_text="Diabète, hypertension, etc.")
    family_history = models.TextField(blank=True, help_text="Maladies héréditaires dans la famille")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dossier médical de {self.patient}"

class Allergy(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Faible'),
        ('MEDIUM', 'Moyenne'),
        ('HIGH', 'Sévère (Urgence)'),
    ]

    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='allergies')
    allergen = models.CharField(max_length=100, help_text="Nom de l'allergène (ex: Pénicilline, Arachides)")
    reaction = models.TextField(blank=True, help_text="Type de réaction (ex: éruption cutanée, choc anaphylactique)")
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='MEDIUM')
    discovered_on = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.allergen} ({self.get_severity_display()})"


class SurgeryHistory(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='surgeries')
    procedure_name = models.CharField(max_length=200, help_text="Nom de l'intervention (ex: Appendicectomie)")
    surgery_date = models.DateField(blank=True, null=True)
    hospital_name = models.CharField(max_length=150, blank=True, help_text="Où l'opération a eu lieu")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.procedure_name} - {self.surgery_date}"
