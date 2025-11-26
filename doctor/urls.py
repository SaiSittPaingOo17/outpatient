from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('', views.doctor_home_redirect, name='home'),
    path('doctor_dashboard/',views.doctor_dashboard,name="doctor_dashboard"),
    path('doctor_login/', views.doctor_login, name="doctor_login"),
    path('doctor_logout/', views.doctor_logout, name='doctor_logout'),
    path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
    path('edit_password/', views.edit_password, name='edit_password'),
    path('doctor_search/', views.doctor_search, name='doctor_search'),
] 