from django.urls import path
from . import views

app_name = 'patient'
urlpatterns = [
    path('', views.index, name='index'),
    path('patient_register', views.patient_register, name='patient_register'),
    path('patient_login', views.patient_login, name="patient_login"),
    path('patient_logout', views.patient_logout, name="patient_logout")
]