# medical_records/admin.py
from django.contrib import admin
from .models import MedicalRecord, Allergy, SurgeryHistory

admin.site.register([MedicalRecord, Allergy, SurgeryHistory])
