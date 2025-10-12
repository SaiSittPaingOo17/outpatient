from django.urls import path
from . import views

app_name = 'consultation'

urlpatterns = [
    path('',views.index, name='index'),
    path('show_triage/', views.show_triage, name='show_triage'),
    path('record/<int:triage_id>', views.record, name='record'),
    path('show_consultation/', views.show_consultation, name='show_consultation'),
    path('edit_consultation/<int:consultation_id>', views.edit_consultation,name='edit_consultation'),
    path('make_prescription/<int:consultation_id>', views.make_prescription, name='make_prescription'),
]