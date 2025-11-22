# decorators.py
from functools import wraps
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from pharmacist.models import Pharmacist

def pharmacist_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        pharmacist_id = request.session.get('pharmacist_id')

        if not pharmacist_id:
            messages.error(request, 'Please log in first.')
            return HttpResponseRedirect(reverse('pharmacist:pharmacist_login'))
        
        try:
            pharmacist = Pharmacist.objects.get(id=pharmacist_id)
            request.pharmacist = pharmacist
            return view_func(request, *args, **kwargs)
        except Pharmacist.DoesNotExist:
            
            messages.error(request, 'User Not Found. Please log in again.')
            return HttpResponseRedirect(reverse('pharmacist:pharmacist_login'))
        
    return wrapper