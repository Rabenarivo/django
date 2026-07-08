from django.shortcuts import render, redirect, get_object_or_404
from appointments.models import Appointment
from .models import Consultation
from .forms import ConsultationForm
from doctors.models import Doctor
from django.contrib.auth.decorators import login_required


@login_required
def list_consultation(request):
    consultations = Consultation.objects.all()
    return render(request, 'consultation/list_consultation.html', {
        'consultations': consultations
    })


@login_required
def list_consultation_doctor(request):
    doctor = Doctor.objects.filter(user=request.user).first()
    if not doctor:
        return redirect('home')
    all_appointments = Appointment.objects.all()
    
    appointments = Appointment.objects.filter(doctor=doctor, status='Confirmed')
    print(f"Filtered appointments: {appointments}")
    
    consultations = Consultation.objects.filter(appointment__doctor=doctor)
    print(f"Consultations: {consultations}")
    
    form = ConsultationForm()
    form.fields['appointment'].queryset = appointments
    
    return render(request, 'consultation/list_consultation_doctor.html', {
        'appointments': appointments,
        'consultations': consultations,
        'form': form,
        'debug_info': {
            'user': request.user,
            'doctor': doctor,
            'all_appointments_count': all_appointments.count(),
            'filtered_appointments_count': appointments.count()
        }
    })


@login_required
def create_consultation(request, appointment_id=None):
    doctor = Doctor.objects.filter(user=request.user).first()
    if not doctor:
        return redirect('home')
    confirmed_appointments = Appointment.objects.filter(doctor=doctor, status='Confirmed')
    
    # Get the appointment if ID is provided
    selected_appointment = None
    if appointment_id:
        selected_appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor, status='Confirmed')
    
    if request.method == 'POST':
        print("POST request received!")
        form = ConsultationForm(request.POST)
        print(f"Form valid? {form.is_valid()}")
        if form.is_valid():
            consultation = form.save()
            print(f"Consultation created with ID: {consultation.id}")
            return redirect('create_prescription_for_consultation', consultation_id=consultation.id)
        else:
            print(f"Form errors: {form.errors}")
    else:
        # Pre-fill the form with the selected appointment if available
        if selected_appointment:
            form = ConsultationForm(initial={'appointment': selected_appointment})
        else:
            form = ConsultationForm()
    
    medical_profile = None
    if selected_appointment and hasattr(selected_appointment.patient, 'medical_profile'):
        medical_profile = selected_appointment.patient.medical_profile

    form.fields['appointment'].queryset = confirmed_appointments
    return render(request, 'consultation/create_consultation.html', {
        'form': form,
        'selected_appointment': selected_appointment,
        'medical_profile': medical_profile
    })


@login_required
def consultation_detail(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    return render(request, 'consultation/consultation_detail.html', {
        'consultation': consultation
    })

