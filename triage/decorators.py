# decorators.py
from functools import wraps
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from nurse.models import Nurse

def nurse_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        nurse_id = request.session.get('nurse_id')

        if not nurse_id:
            messages.error(request, 'Please log in first.')
            return HttpResponseRedirect(reverse('nurse:nurse_login'))
        
        try:
            nurse = Nurse.objects.get(id=nurse_id)
            request.nurse = nurse
            return view_func(request, *args, **kwargs)
        except Nurse.DoesNotExist:
            
            messages.error(request, 'User Not Found. Please log in again.')
            return HttpResponseRedirect(reverse('nurse:nurse_login'))
        
    return wrapper