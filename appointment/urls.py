from django.urls import path
from . import views

app_name = 'appointment'

urlpatterns = [
    path('', views.index, name='index'),
    
    # Patient-side
    path('search/', views.search_doctors, name='search_doctors'),
    path('doctor/<int:doctor_id>/availability/', views.patient_view_availability, name='patient_view_availability'),
    path('book/<int:availability_id>/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.view_appointments, name='view_appointments'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    
    # Doctor-side
    path('doctor/availability/', views.doctor_availability_view, name='availability'),
    path('doctor/availability/add/', views.add_availability, name='add_availability'),
    path('doctor/availability/delete/<int:availability_id>/', views.delete_availability, name='delete_availability'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('doctor/appointments/confirm/<int:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),
    path('doctor/appointments/cancel/<int:appointment_id>/', views.cancel_appointment_doctor, name='cancel_appointment_doctor'),
]