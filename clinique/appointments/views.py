from django.shortcuts import render
from .models import Appoitments
# Create your views here.

def home_view(request): 
    if request.user.is_authenticated:
        return render(request, 'template/home.html')
    else:
        return render(request, 'accounts/login.html')
    name='appointments_home'
    return render(request, 'template/home.html', {'name': name})   

def create_appointment(request):
    if request.method == 'POST':
        form = AppoitmentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments:home')
    else:
        form = AppoitmentsForm()
    return render(request, 'template/create.html', {'form': form})


