# d:\ITU\django\clinique\appointments\views.py
from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm
from patients.models import Patient
from django.contrib.auth.decorators import login_required


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
    
    return render(request, 'create.html', {'form': form})

@login_required
def list_consultation(request):
    appointment = Appointment.objects.all()
    return render(request, 'appointments/list_consultation.html', {'appointment': appointment})
   