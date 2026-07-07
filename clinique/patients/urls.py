from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('create/', views.create_patient, name='create_patient'),
]
