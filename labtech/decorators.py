# decorators.py
from functools import wraps
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from labtech.models import LabTechnician

def labtech_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        labtech_id = request.session.get('labtech_id')

        if not labtech_id:
            messages.error(request, 'Please log in first.')
            return HttpResponseRedirect(reverse('labtech:labtech_login'))
        
        try:
            labtech = LabTechnician.objects.get(id=labtech_id)
            request.labtech = labtech
            return view_func(request, *args, **kwargs)
        except LabTechnician.DoesNotExist:
            
            messages.error(request, 'User Not Found. Please log in again.')
            return HttpResponseRedirect(reverse('labtech:labtech_login'))
        
    return wrapper