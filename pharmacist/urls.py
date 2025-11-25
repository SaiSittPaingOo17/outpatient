from django.urls import path
from . import views

app_name = 'pharmacist'

urlpatterns = [
    path('',views.pharmacist_home_redirect, name='home'),
    path('pharmacist_login/', views.pharmacist_login, name='pharmacist_login'),
    path('pharmacist_logout/', views.pharmacist_logout, name='pharmacist_logout'),
    path('pharmacist_dashboard/', views.pharmacist_dashboard, name='pharmacist_dashboard'),
    path('show_medications/', views.show_medications, name='show_medications'),
    path('update_status/<int:prescription_id>/', views.update_status, name='update_status'),
    path('pharmacist_search/', views.pharmacist_search, name='pharmacist_search'),
]