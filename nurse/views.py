from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Nurse


from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password

def dashboard(request):
    return render(request, 'nurse/dashboard.html')

# nurse authentication
def nurse_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        try:
            nurse = Nurse.objects.get(email=email)

            print("Stored password:", nurse.password)
            print("Entered password:", password)

            if check_password(password, nurse.password):
                request.session['nurse_id'] = nurse.id
                request.session['nurse_email'] = nurse.email
                messages.success(request, 'Login Succeeds!')
                return HttpResponseRedirect(reverse('triage:show_appointments'))
            else:
                messages.error(request, 'Invalid Email or Password')
                return render(request, 'nurse/nurse_login.html')

        except Nurse.DoesNotExist:
            messages.error(request, 'The user does not exist')
            return render(request, 'nurse/nurse_login.html')

        except Exception as e:
            messages.error(request, f'Error: {e}')
            return render(request, 'nurse/nurse_login.html')

    return render(request, 'nurse/nurse_login.html')
