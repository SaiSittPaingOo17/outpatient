from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'patient'
urlpatterns = [
    # setting login page as default page
    path('', RedirectView.as_view(pattern_name='patient:patient_login'), name='index'),
    path('patient_register/', views.patient_register, name='patient_register'),
    path('patient_login/', views.patient_login, name="patient_login"),
    path('patient_logout/', views.patient_logout, name="patient_logout")
]