from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from doctor.models import Doctor
from patient.models import Patient

def doctor_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        doctor_id = request.session.get('doctor_id')
        if not doctor_id:
            messages.error(request, 'Please log in first')
            return HttpResponseRedirect(reverse('doctor:doctor_login'))
        
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            request.doctor = doctor  # Attach doctor to request
            return view_func(request, *args, **kwargs)
        except Doctor.DoesNotExist:
            messages.error(request, 'Doctor not found')
            return HttpResponseRedirect(reverse('doctor:doctor_login'))
    
    return wrapper

def patient_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        patient_id = request.session.get('patient_id')
        if not patient_id:
            messages.error(request, 'Please log in first')
            return HttpResponseRedirect(reverse('patient:patient_login'))
        
        try:
            patient = Patient.objects.get(id=patient_id)
            request.patient = patient  # Attach patient to request
            return view_func(request, *args, **kwargs)
        except Patient.DoesNotExist:
            messages.error(request, 'User not found')
            return HttpResponseRedirect(reverse('patient:patient_login'))
    
    return wrapper
