from django.urls import path
from . import views

app_name = 'nurse'

urlpatterns = [
    path('', views.nurse_home_redirect, name='home'),
    path('nurse_dashboard/', views.nurse_dashboard, name='nurse_dashboard'),
    path('nurse_login/', views.nurse_login, name='nurse_login'),
    path('nurse_logout', views.nurse_logout, name='nurse_logout'),
    path('nurse_search', views.nurse_search, name='nurse_search'),
]