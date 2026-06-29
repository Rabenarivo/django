from django.contrib import admin
from django.urls import path, include
from accounts.views import home_view
from consultations.models import Consultation

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('appointments/', include('appointments.urls')),
    path('consultations/', include('consultations.urls')),
]