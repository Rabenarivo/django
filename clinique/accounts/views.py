from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render
from .models import Profile
from .forms import CustomUserCreationForm
from patients.models import Patient
from appointments.forms import AppointmentForm
from appointments.models import Appointment 


def home_view(request):
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)

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
            # GET request - create empty form
            form = AppointmentForm()
        
        # Render the form
        if profile and (profile.role == 'CLIENT' or profile.role == 'client'):
            return render(request, 'create.html', {
                'user': request.user,
                'profile': profile,
                'form': form,
            })
        return render(request, 'create.html', {
            'user': request.user,
            'profile': profile,
            'form': form,
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

