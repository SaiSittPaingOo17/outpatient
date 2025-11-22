from django.urls import path
from . import views

app_name = 'pharmacist'

urlpatterns = [
    path('pharmacist_login/', views.pharmacist_login, name='pharmacist_login'),
    path('pharmacist_logout/', views.pharmacist_logout, name='pharmacist_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('show_medications/', views.show_medications, name='show_medications'),
    path('update_status/<int:prescription_id>/', views.update_status, name='update_status'),

]