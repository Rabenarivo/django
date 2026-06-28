from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_consultation, name='list_consultation'),
]
