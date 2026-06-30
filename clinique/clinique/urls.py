from django.contrib import admin
from django.urls import path, include
from accounts.views import home_view
from consultations.models import Consultation
from medicines.models import Medicine



urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('appointments/', include('appointments.urls')),
    path('consultations/', include('consultations.urls')),
    path('prescriptions/', include('prescriptions.urls')),
    path('medicines/', include('medicines.urls')),
]