from django import forms
from .models import MedicalRecord, Allergy, SurgeryHistory

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'blood_group', 'chronic_diseases', 'family_history']

class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = ['record', 'allergen', 'reaction', 'severity', 'discovered_on']

class SurgeryHistoryForm(forms.ModelForm):
    class Meta:
        model = SurgeryHistory
        fields = ['record', 'procedure_name', 'surgery_date', 'hospital_name', 'notes']