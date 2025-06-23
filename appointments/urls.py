from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:apt_id>/appointment", views.appointment, name="appointment"),
    path("<int:dept_id>/department", views.department, name="department"),
    path("<int:dept_id>/assign_doctor", views.assign_doctor, name="assign_doctor")
]