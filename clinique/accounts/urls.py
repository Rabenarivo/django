from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='accounts_home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_user, name='create_user'),
    path('admin/statistics/', views.admin_statistics_view, name='admin_statistics'),
]