from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from doctor.models import Doctor

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