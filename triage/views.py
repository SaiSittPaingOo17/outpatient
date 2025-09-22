from django.shortcuts import render
from appointment.models import Appointment
from .models import Nurse 
from .decorators import nurse_login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    return render(request, 'triage/index.html')

@nurse_login_required
def show_appointments(request):
    nurse = request.nurse
    nurse_department = nurse.department
    
    appointments = Appointment.objects.filter(
        doctor__department=nurse_department
    ).select_related('doctor', 'patient')

    return render(request, 'triage/show_appointments.html', {
        'appointments': appointments,
    })

def fill_triage(request):
    nurse = request.nurse
    nurse_department = nurse.department
    
    appointments = Appointment.objects.filter(
        doctor__department=nurse_department
    ).select_related('doctor', 'patient')

    return render(request, 'triage/fill_triage.html',{
        appointment
    })