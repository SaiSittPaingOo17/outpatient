from django.urls import path
from . import views

app_name = 'appointment'

urlpatterns = [
    path('',views.index, name='index'),
    # Patient-side
    path('search/', views.search_doctors, name='search_doctors'),
    path('availability/<int:doctor_id>/', views.view_availability, name='view_availability'),
    path('book/<int:availability_id>/', views.book_appointment, name='book_appointment'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),

    # Doctor-side
    path('doctor/availability/', views.doctor_availability_view, name='availability'),
    path('doctor/availability/add/', views.add_availability, name='add_availability'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('doctor/appointments/confirm/<int:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),
]

