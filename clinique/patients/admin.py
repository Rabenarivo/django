from django.contrib import admin
from .models import Patient, MedicalProfile

admin.site.register(Patient)
admin.site.register(MedicalProfile)
