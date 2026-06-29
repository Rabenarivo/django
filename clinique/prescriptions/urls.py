from django.urls import path
from . import views

urlpatterns = [
    path('doctor/list/', views.list_prescriptions_doctor, name='list_prescriptions_doctor'),
    path('create/', views.create_prescription, name='create_prescription'),
    path('create/<int:consultation_id>/', views.create_prescription, name='create_prescription_for_consultation'),
    path('detail/<int:prescription_id>/', views.prescription_detail, name='prescription_detail'),
]
