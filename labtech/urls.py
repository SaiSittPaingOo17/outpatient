from django.urls import path
from . import views

app_name = 'labtech'

urlpatterns = [
    path('labtech_login/', views.labtech_login, name='labtech_login'),
    path('labtech_logout/', views.labtech_logout, name='labtech_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('show_tests/', views.show_tests ,name='show_tests'),
    path('update_status/<int:prescription_id>/', views.update_status, name='update_status'),
]