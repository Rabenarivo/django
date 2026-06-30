from django.shortcuts import render, redirect, get_object_or_404
from .models import Prescription, PrescriptionItem
from .forms import PrescriptionForm, PrescriptionItemForm
from consultations.models import Consultation
from medicines.models import Medicine, StockMovement
from doctors.models import Doctor
from django.contrib.auth.decorators import login_required


@login_required
def list_prescriptions_doctor(request):
    doctor = Doctor.objects.filter(user=request.user).first()
    if not doctor:
        return redirect('home')
    prescriptions = Prescription.objects.filter(consultation__appointment__doctor=doctor)
    return render(request, 'prescriptions/list_prescriptions.html', {
        'prescriptions': prescriptions
    })


@login_required
def create_prescription(request, consultation_id=None):
    doctor = Doctor.objects.filter(user=request.user).first()
    if not doctor:
        return redirect('home')
    
    consultations = Consultation.objects.filter(appointment__doctor=doctor)
    medicines = Medicine.objects.all()
    
    selected_consultation = None
    if consultation_id:
        selected_consultation = get_object_or_404(Consultation, id=consultation_id, appointment__doctor=doctor)
    
    if request.method == 'POST':
        # Get consultation
        consultation_id_post = request.POST.get('consultation')
        consultation = get_object_or_404(Consultation, id=consultation_id_post, appointment__doctor=doctor)
        
        # Create prescription
        prescription = Prescription.objects.create(consultation=consultation)
        
        # Get items data from POST
        medicine_ids = request.POST.getlist('medicine')
        quantities = request.POST.getlist('quantity')
        dosages = request.POST.getlist('dosage')
        frequencies = request.POST.getlist('frequency')
        durations = request.POST.getlist('duration')
        
        # Create PrescriptionItem for each medicine and update stock
        for i in range(len(medicine_ids)):
            if medicine_ids[i]:  # Only create if medicine is selected
                medicine = Medicine.objects.get(id=medicine_ids[i])
                qty = int(quantities[i]) if quantities[i] else 1
                
                # Create PrescriptionItem
                PrescriptionItem.objects.create(
                    prescription=prescription,
                    medicine=medicine,
                    quantity=qty,
                    dosage=dosages[i],
                    frequency=frequencies[i],
                    duration=durations[i]
                )
                
                # Create StockMovement (OUT)
                StockMovement.objects.create(
                    medicine=medicine,
                    movement_type='OUT',
                    quantity=qty,
                    reference=f"Prescription {prescription.id}"
                )
        
        return redirect('prescription_detail', prescription_id=prescription.id)
    
    return render(request, 'prescriptions/create_prescription.html', {
        'consultations': consultations,
        'medicines': medicines,
        'selected_consultation': selected_consultation
    })


@login_required
def prescription_detail(request, prescription_id):
    doctor = Doctor.objects.filter(user=request.user).first()
    if not doctor:
        return redirect('home')
    
    prescription = get_object_or_404(Prescription, id=prescription_id, consultation__appointment__doctor=doctor)
    
    return render(request, 'prescriptions/prescription_detail.html', {
        'prescription': prescription
    })
