from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Pharmacist
from .decorators import pharmacist_login_required

from django.contrib import messages
from django.contrib.auth.hashers import check_password

from consultation.models import Prescription, PrescriptionType

# pharmacist authentication
def pharmacist_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        try:
            pharmacist = Pharmacist.objects.get(email=email)

            print("Stored password:", pharmacist.password)
            print("Entered password:", password)

            if check_password(password, pharmacist.password):
                request.session['pharmacist_id'] = pharmacist.id
                request.session['pharmacist_email'] = pharmacist.email
                messages.success(request, 'Login Succeeds!')
                return HttpResponseRedirect(reverse('pharmacist:show_medications'))
            else:
                messages.error(request, 'Invalid Email or Password')
                return render(request, 'pharmacist/pharmacist_login.html')

        except Pharmacist.DoesNotExist:
            messages.error(request, 'The user does not exist')
            return render(request, 'pharmacist/pharmacist_login.html')

        except Exception as e:
            messages.error(request, f'Error: {e}')
            return render(request, 'pharmacist/pharmacist_login.html')

    return render(request, 'pharmacist/pharmacist_login.html')

def pharmacist_logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return HttpResponseRedirect(reverse('pharmacist:pharmacist_login'))

# Create your views here.
@pharmacist_login_required
def dashboard(request):
    pharmacist = request.pharmacist
    return render(request, 'pharmacist/dashboard.html',{
        'pharmacist': pharmacist,
    })


@pharmacist_login_required
def show_medications(request):
    pharmacist = request.pharmacist

    # Medication type
    med_type = PrescriptionType.objects.get(prescription_type='medication')

    # All medication prescriptions
    medications = Prescription.objects.filter(prescription_type=med_type)

    return render(request, 'pharmacist/show_medications.html', {
        'pharmacist': pharmacist,
        'medications': medications,
    })

@pharmacist_login_required
def update_status(request, prescription_id):
    pharmacist = request.pharmacist
    prescription = get_object_or_404(Prescription, id=prescription_id)

    if request.method == "POST":
        prescription.status = request.POST.get("status")
        prescription.save()
        messages.success(request, "Medication status updated successfully!")
        return HttpResponseRedirect(reverse('pharmacist:show_medications'))

    return render(request, 'pharmacist/update_status.html', {
        'pharmacist': pharmacist,
        'prescription': prescription,
    })
