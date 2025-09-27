from django.urls import path
from . import views

app_name = 'triage'
urlpatterns = [
    path('', views.index, name='index'),
    path('show_appointments/', views.show_appointments, name='show_appointments'),
    path('fill_triage/<int:appointment_id>/', views.fill_triage, name='fill_triage'),
    path('triage/', views.log, name='log'),
    path('triage_details/<int:triage_id>', views.triage_details, name='triage_details'),
    path('edit_triage/<int:triage_id>',views.edit_triage, name='edit_triage'),
]