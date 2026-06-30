# d:\ITU\django\clinique\appointments\views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment
from .forms import AppointmentForm
from patients.models import Patient
from doctors.models import Doctor  # Add this import
from django.contrib.auth.decorators import login_required
from django import forms  # For the form


# Create a simple form to assign a doctor
class AssignDoctorForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor']


@login_required
def home_view(request):
    return redirect('create_appointment')


@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            patient = Patient.objects.filter(user=request.user).first()
            if patient:
                appointment.patient = patient
                appointment.save()
                return redirect('home')
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/create.html', {'form': form})


@login_required
def list_consultation(request):
    appointments = Appointment.objects.filter(status__in=['Pending', 'Confirmed'])
    return render(request, 'appointments/list_consultation.html', {'appointments': appointments})


@login_required
def assign_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user is receptionist
    profile = getattr(request.user, 'profile', None)
    if not (profile and profile.role == 'RECEPTIONIST'):
        return redirect('home')
    
    if request.method == 'POST':
        form = AssignDoctorForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = 'Confirmed'  # Use the correct status from model
            appointment.save()
            return redirect('list_consultation')
    else:
        form = AssignDoctorForm(instance=appointment)
    
    return render(request, 'appointments/assign_appointment.html', {'form': form, 'appointment': appointment})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Cancelled'
    appointment.save()
    return redirect('list_consultation')
