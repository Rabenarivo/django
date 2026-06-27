from django.contrib import admin
from django.urls import path
from accounts.views import home_view, login_view, logout_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', home_view, name='accounts_home'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
]