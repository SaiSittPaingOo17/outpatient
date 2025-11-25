from django.urls import path
from . import views

app_name = 'labtech'

urlpatterns = [
    path('', views.labtech_home_redirect, name='home'),
    path('labtech_login/', views.labtech_login, name='labtech_login'),
    path('labtech_logout/', views.labtech_logout, name='labtech_logout'),
    path('labtech_dashboard/', views.labtech_dashboard, name='labtech_dashboard'),
    path('show_tests/', views.show_tests ,name='show_tests'),
    path('update_status/<int:prescription_id>/', views.update_status, name='update_status'),
    path('labtech_search/', views.labtech_search, name='labtech_search'),
]