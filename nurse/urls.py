from django.urls import path
from . import views

app_name = 'nurse'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('nurse_login/', views.nurse_login, name='nurse_login'),
    path('nurse_logout', views.nurse_logout, name='nurse_logout'),
]