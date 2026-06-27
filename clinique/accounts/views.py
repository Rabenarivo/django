from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render
from .models import Profile


def home_view(request):
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        return render(request, 'home.html', {
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

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')



def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'create_user.html', {'form': form})


