from django.shortcuts import render,redirect,get_object_or_404
from patients.models import Patient
from .models import MedicalRecord, Allergy, SurgeryHistory
from .forms import MedicalRecordForm, AllergyForm, SurgeryHistoryForm

# Create your views here.
@login_required
def create_medical_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=patient_id)
    else:
        form = MedicalRecordForm()
    return render(request, 'medical_record/create_medical_record.html', {
        'form': form
    })

@login_required
def create_allergy(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = AllergyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=patient_id)
    else:
        form = AllergyForm()
    return render(request, 'medical_record/create_allergy.html', {
        'form': form
    })

@login_required
def create_surgery_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = SurgeryHistoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=patient_id)
    else:
        form = SurgeryHistoryForm()
    return render(request, 'medical_record/create_surgery_history.html', {
        'form': form
    })