from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import LabTechnician
from .decorators import labtech_login_required

from django.contrib import messages
from django.contrib.auth.hashers import check_password

from consultation.models import Prescription, PrescriptionType

# labtechnician authentication
def labtech_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        try:
            labtech = LabTechnician.objects.get(email=email)

            print("Stored password:", labtech.password)
            print("Entered password:", password)

            if check_password(password, labtech.password):
                request.session['labtech_id'] = labtech.id
                request.session['labtech_email'] = labtech.email
                messages.success(request, 'Login Succeeds!')
                return HttpResponseRedirect(reverse('labtech:show_tests'))
            else:
                messages.error(request, 'Invalid Email or Password')
                return render(request, 'labtech/labtech_login.html')

        except LabTechnician.DoesNotExist:
            messages.error(request, 'The user does not exist')
            return render(request, 'labtech/labtech_login.html')

        except Exception as e:
            messages.error(request, f'Error: {e}')
            return render(request, 'labtech/labtech_login.html')

    return render(request, 'labtech/labtech_login.html')

def labtech_logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return HttpResponseRedirect(reverse('labtech:labtech_login'))

@labtech_login_required
def dashboard(request):
    labtech = request.labtech
    return render(request,'labtech/dashboard.html',{
        'labtech': labtech,
    })

# Tests
@labtech_login_required
def show_tests(request):
    labtech = request.labtech

    # laboratory type
    lab_type = PrescriptionType.objects.get(prescription_type='laboratory')

    # ALL laboratory prescriptions
    lab_tests = Prescription.objects.filter(prescription_type=lab_type)

    return render(request, 'labtech/show_tests.html', {
        'labtech': labtech,
        'lab_tests': lab_tests,
    })

@labtech_login_required
def update_status(request, prescription_id):
    labtech = request.labtech
    prescription = get_object_or_404(Prescription, id=prescription_id)

    if request.method == "POST":
        prescription.status = request.POST.get("status")
        prescription.save()
        messages.success(request, "Status updated successfully!")
        return HttpResponseRedirect(reverse('labtech:show_tests'))

    return render(request, 'labtech/update_status.html', {
        'labtech': labtech,
        'prescription': prescription,
    })
