from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='appointments_home'),
    path('create/', views.create_appointment, name='create_appointment'),
    path('list/', views.list_consultation, name='list_consultation'),
]
