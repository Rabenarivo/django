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
                return render(request, 'accounts/home_admin.html', {
                    'user': request.user,
                    'profile': profile,
                })
            elif role == 'DOCTOR':
                return render(request, 'accounts/home_doctor.html', {
                    'user': request.user,
                    'profile': profile,
                })
            elif role == 'CLIENT':
                return render(request, 'accounts/home_client.html', {
                    'user': request.user,
                    'profile': profile,
                    'form': form,
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

