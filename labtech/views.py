from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import LabTechnician
from .decorators import labtech_login_required

from django.contrib import messages
from django.contrib.auth.hashers import check_password

from consultation.models import Prescription, PrescriptionType
from triage.models import Triage

from django.db.models import Q

def labtech_home_redirect(request):
    return redirect('labtech:labtech_dashboard')

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
def labtech_profile(request):
    labtech_id = request.session.get('labtech_id')
    labtech = get_object_or_404(LabTechnician, id=labtech_id)
    return render(request, 'labtech/profile.html', {'labtech': labtech})

@labtech_login_required
def labtech_change_password(request):
    labtech_id = request.session.get('labtech_id')
    labtech = get_object_or_404(LabTechnician, id=labtech_id)

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password     = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Validate current password
        if not labtech.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('labtech:change_password')

        # Check new password match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('labtech:change_password')

        # Save new password
        labtech.user.set_password(new_password)
        labtech.user.save()

        messages.success(request, "Password updated successfully.")
        return redirect('labtech:profile')

    return render(request, 'labtech/change_password.html', {'labtech': labtech})

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

@labtech_login_required
def labtech_dashboard(request):
    labtech = request.labtech

    lab_type = PrescriptionType.objects.get(prescription_type='laboratory')
    tests = Prescription.objects.filter(prescription_type=lab_type)

    total_tests = tests.count()
    pending_tests = tests.filter(status='pending').count()
    processing_tests = tests.filter(status='processing').count()
    completed_tests = tests.filter(status='completed').count()

    recent_tests = tests.order_by("-created_at")[:5]

    return render(request, 'labtech/labtech_dashboard.html', {
        'labtech': labtech,
        'total_tests': total_tests,
        'pending_tests': pending_tests,
        'processing_tests': processing_tests,
        'completed_tests': completed_tests,
        'recent_tests': recent_tests,
    })

@labtech_login_required
def labtech_search(request):
    labtech = request.labtech

    raw_date = request.GET.get("search_date", "").strip()
    search_date = raw_date if raw_date else None
    search_name = request.GET.get("search_name", "").strip()
    search_id = request.GET.get("search_id", "").strip()

    # only laboratory prescriptions
    lab_type = PrescriptionType.objects.get(prescription_type="laboratory")
    qs = Prescription.objects.filter(prescription_type=lab_type)

    # filtering
    if search_date:
        qs = qs.filter(created_at__date=search_date)

    if search_name:
        qs = qs.filter(
            Q(consultation__appointment__patient__fname__icontains=search_name) |
            Q(consultation__appointment__patient__lname__icontains=search_name)
        )

    if search_id:
        qs = qs.filter(id=search_id)

    results = qs.order_by("-created_at")

    return render(request, "labtech/labtech_search.html", {
        "labtech": labtech,
        "results": results,
        "search_date": search_date,
        "search_name": search_name,
        "search_id": search_id,
    })
