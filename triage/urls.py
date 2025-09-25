from django.urls import path
from . import views

app_name = 'triage'
urlpatterns = [
    path('', views.index, name='index'),
    path('show_appointments/', views.show_appointments, name='show_appointments'),
    path('fill_triage/<int:appointment_id>/', views.fill_triage, name='fill_triage'),
    path('triage/', views.log, name='log'),
]