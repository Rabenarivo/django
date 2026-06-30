from django.urls import path
from . import views

urlpatterns = [
    path('change_statut_sale/<int:sale_id>/', views.chabge_statut_sale, name='change_statut_sale'),
    path('list_sales/', views.list_sales, name='list_sales'),
]
