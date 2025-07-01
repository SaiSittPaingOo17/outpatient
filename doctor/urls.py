from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('dashboard/',views.dashboard,name="dashboard"),
    path('doctor_login/', views.doctor_login, name="doctor_login"),
    path('doctor_logout/', views.doctor_logout, name='doctor_logout'),
]