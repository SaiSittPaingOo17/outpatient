from django.urls import path
from . import views

app_name = 'consultation'

urlpatterns = [
    path('',views.index, name='index'),
    path('show_triage/', views.show_triage, name='show_triage'),
    path('record/<int:triage_id>', views.record, name='record'),
    path('show_consultation/', views.show_consultation, name='show_consultation'),
    path('edit_consultation/<int:consultation_id>', views.edit_consultation,name='edit_consultation'),
    path('make_prescription/<int:consultation_id>/', views.make_prescription, name='make_prescription'),
    path('view_prescription/<int:consultation_id>/', views.view_prescription, name='view_prescription'),
    path('edit_prescription/<int:prescription_id>/', views.edit_prescription, name='edit_prescription'),
    path('delete_prescription/<int:prescription_id>/', views.delete_prescription, name='delete_prescription'),


]