from django.urls import path
from . import views

app_name = 'triage'
urlpatterns = [
    path('', views.index, name='index'),
    path('show_appointments/', views.show_appointments, name='show_appointments'),
    path('fill_triage/', views.fill_triage, name='fill_triage')

]