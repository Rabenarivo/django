from django.urls import path
from . import views

urlpatterns = [
    path('change_statut_sale/<int:sale_id>/', views.chabge_statut_sale, name='change_statut_sale'),
    path('list_sales/', views.list_sales, name='list_sales'),
    path('create_medicine/', views.create_medicine, name='create_medicine'),
    path('create_medicine_stock/', views.create_medicine_stock, name='create_medicine_stock'),
    path('create_medicine_stock/<int:medicine_id>/', views.create_medicine_stock, name='create_medicine_stock_1')

]
