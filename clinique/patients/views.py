from django.shortcuts import render, redirect
from .forms import PatientForm, MedicalProfileForm

def create_patient(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        profile_form = MedicalProfileForm(request.POST)
        
        if patient_form.is_valid() and profile_form.is_valid():
            patient = patient_form.save()
            profile = profile_form.save(commit=False)
            profile.patient = patient
            profile.save()
            
            return redirect('home')
    else:
        patient_form = PatientForm()
        profile_form = MedicalProfileForm()

    context = {
        'patient_form': patient_form,
        'profile_form': profile_form
    }
    return render(request, 'patients/create_patient.html', context)
