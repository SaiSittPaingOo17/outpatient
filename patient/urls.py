from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'patient'
urlpatterns = [
    # setting login page as default page
    path('', views.patient_home_redirect, name='home'),
    path('patient_register/', views.patient_register, name='patient_register'),
    path('patient_login/', views.patient_login, name="patient_login"),
    path('patient_logout/', views.patient_logout, name="patient_logout"),
    path('patient_profile/', views.patient_profile, name='patient_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('payments/', views.patient_payments, name='patient_payments'),
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('search/', views.patient_search, name='patient_search'),


]