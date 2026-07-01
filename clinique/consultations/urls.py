from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_consultation, name='list_consultation'),
    path('doctor/list/', views.list_consultation_doctor, name='list_consultation_doctor'),
    path('create/', views.create_consultation, name='create_consultation'),
    path('create/<int:appointment_id>/', views.create_consultation, name='create_consultation_for_appointment'),
]
