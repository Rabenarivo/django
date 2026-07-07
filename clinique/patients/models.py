from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    GENDER = [
        ('M', 'Masculin'),
        ('F', 'Féminin')
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    blood_group = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class MedicalProfile(models.Model):
    """
    Le Profil Médical Permanent (Le "Synthétique")
    Informations cruciales visibles en un coup d'œil.
    """
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='medical_profile')
    
    medical_history = models.TextField(
        blank=True, 
        verbose_name="Antécédents médicaux", 
        help_text="Maladies chroniques (diabète, hypertension, etc.), hospitalisations passées."
    )
    
    surgical_history = models.TextField(
        blank=True, 
        verbose_name="Antécédents chirurgicaux", 
        help_text="Opérations subies (avec dates si possible)."
    )
    
    family_history = models.TextField(
        blank=True, 
        verbose_name="Antécédents familiaux", 
        help_text="Maladies héréditaires ou récurrentes dans la famille (ex: maladies cardiaques, cancers)."
    )
    
    allergies = models.TextField(
        blank=True, 
        verbose_name="Allergies et contre-indications", 
        help_text="Médicaments (ex: pénicilline), aliments, latex. Indispensable pour bloquer une mauvaise prescription."
    )
    
    risk_factors = models.TextField(
        blank=True, 
        verbose_name="Facteurs de risque / Mode de vie", 
        help_text="Tabagisme, consommation d'alcool, profession (exposition à des risques). Le groupe sanguin est déjà dans le modèle Patient."
    )
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profil Synthétique - {self.patient}"