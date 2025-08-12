from django.shortcuts import render

from appointment.models import Appointment, Patient
from doctor.models import Doctor, Department
from .models import Nurse 

def index(request):
    return render(request, 'triage/index.html')

def show_appointments(request):

    # appointment = Appointment.objects.get(retrieve appointment according to department of nurse)
     

    return render(request, 'triage/show_appointments.html')

def fill_triage(request):
    return render(request, 'triage/fill_triage.html')