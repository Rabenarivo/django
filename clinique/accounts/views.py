import json
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render
from .models import Profile
from .forms import CustomUserCreationForm
from patients.models import Patient
from appointments.forms import AppointmentForm
from appointments.models import Appointment 


# d:\ITU\django\clinique\accounts\views.py
def home_view(request):
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        
        # Handle POST request only if it's a CLIENT (since only clients create appointments)
        if request.method == 'POST' and profile and profile.role.upper() == 'CLIENT':
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
        
        # Determine which template to render based on role
        if profile:
            role = profile.role.upper()
            if role == 'ADMIN':
                from django.contrib.auth.models import User
                from medicines.models import Sale
                
                # Statistics
                pending_count = Appointment.objects.filter(status='Pending').count()
                confirmed_count = Appointment.objects.filter(status='Confirmed').count()
                users_count = User.objects.count()
                sales_count = Sale.objects.count()

                # Calendar events
                events = []
                all_appointments = Appointment.objects.all()
                for appt in all_appointments:
                    # Determine color based on status
                    if appt.status == 'Confirmed':
                        color = 'green' # "accepté" -> vert
                    elif appt.status == 'Pending':
                        color = '#ffc107' # "non assigné" -> jaune
                    else:
                        color = '#dc3545' # "confirmé" (annulé/autre) -> rouge

                    events.append({
                        'title': f"{appt.patient.first_name} {appt.patient.last_name} ({appt.get_status_display()})",
                        'start': f"{appt.appointment_date}T{appt.appointment_time}",
                        'color': color,
                        'url': f"/appointments/assign/{appt.id}/" if appt.status == 'Pending' else "#"
                    })
                events_json = json.dumps(events, default=str)

                return render(request, 'accounts/home_admin.html', {
                    'user': request.user,
                    'profile': profile,
                    'pending_count': pending_count,
                    'confirmed_count': confirmed_count,
                    'users_count': users_count,
                    'sales_count': sales_count,
                    'events_json': events_json,
                })
            elif role == 'DOCTOR':
                events = []
                doctor = getattr(request.user, 'doctor', None)
                if doctor:
                    # N'afficher que les rendez-vous Confirmés ET qui n'ont pas encore de consultation
                    appointments = Appointment.objects.filter(
                        doctor=doctor, 
                        status='Confirmed',
                        consultation__isnull=True
                    ).distinct()
                    
                    for appt in appointments:
                        events.append({
                            'title': f"{appt.patient.first_name} {appt.patient.last_name}",
                            'start': f"{appt.appointment_date}T{appt.appointment_time}",
                            # URL pour aller vers la consultation (à adapter si besoin)
                            'url': f"/consultations/create/{appt.id}/"
                        })
                events_json = json.dumps(events, default=str)

                return render(request, 'accounts/home_doctor.html', {
                    'user': request.user,
                    'profile': profile,
                    'events_json': events_json,
                })
            elif role == 'RECEPTIONIST':
                return render(request, 'accounts/receptionniste.html', {
                    'user': request.user,
                    'profile': profile,
                })
            elif role == 'CLIENT':
                return render(request, 'accounts/home_client.html', {
                    'user': request.user,
                    'profile': profile,
                    'form': form,
                })
            elif role == 'PHARMARMACIST':
                from medicines.models import Medicine, Sale, StockMovement
                from django.utils import timezone
                
                today = timezone.now().date()
                sales_today_count = Sale.objects.filter(created_at__date=today).count()
                medicines_count = Medicine.objects.count()
                movements_in_count = StockMovement.objects.filter(movement_type='IN').count()
                movements_out_count = StockMovement.objects.filter(movement_type='OUT').count()

                return render(request, 'accounts/home_pharmacist.html', {
                    'user': request.user,
                    'profile': profile,
                    'sales_today_count': sales_today_count,
                    'medicines_count': medicines_count,
                    'movements_in_count': movements_in_count,
                    'movements_out_count': movements_out_count,
                })
        
        # Fallback to default home.html
        return render(request, 'accounts/home_client.html', {
            'user': request.user,
            'profile': profile,
        })
    return redirect('login')
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm(request)

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')



def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            Patient.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                birth_date=form.cleaned_data['birth_date'],
                gender=form.cleaned_data['gender'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                blood_group=form.cleaned_data['blood_group']
            )
            
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/create_user.html', {'form': form})

