from django.urls import path
from . import views

app_name = 'consultation'

urlpatterns = [
    path('',views.index, name='index'),
    path('show_triage/', views.show_triage, name='show_triage'),
    path('record/<int:triage_id>',views.record, name='record'),
]