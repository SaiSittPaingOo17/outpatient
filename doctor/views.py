from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password

from appointment.decorators import doctor_login_required

# models
from .models import Doctor
from consultation.models import Consultation, Prescription
from triage.models import Triage
from appointment.models import Appointment
from django.db.models import Q

# doctor authentication
def doctor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email','')
        password = request.POST.get('password','')

        try:
            doctor = Doctor.objects.get(email=email)
            print(f'From Database: {doctor.password}')
            
            if check_password(password,doctor.password):
                request.session['doctor_id'] = doctor.id
                request.session['doctor_email'] = doctor.email
                messages.success(request,'Login Succeeds!')
                return HttpResponseRedirect(reverse('appointment:availability'))
            else:
                messages.error(request,'Invalid Email or Password')
                return render(request, 'doctor/doctor_login.html')
            
        except Doctor.DoesNotExist:
            messages.error(request,"No doctor found with this email")
            return render(request, 'doctor/doctor_login.html')
        except Exception as e:
            return render(request, 'doctor/doctor_login.html')

    else:
        return render(request,'doctor/doctor_login.html')

# Logout
def doctor_logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return HttpResponseRedirect(reverse('doctor:doctor_login'))

# doctor profile
@doctor_login_required
def doctor_profile(request):
    doctor_id = request.session.get('doctor_id')
    doctor = get_object_or_404(Doctor, id=doctor_id)

    department = doctor.department
    fname = doctor.fname
    lname = doctor.lname
    license = doctor.license
    specialisation = doctor.specialisation
    email = doctor.email
    phone = doctor.phone
    address = doctor.address
    created_at = doctor.created_at
    updated_at = doctor.updated_at 

    return render(request, 'doctor/doctor_profile.html', {
        'department': department,
        'fname': fname,
        'lname': lname,
        'license': license,
        'specialisation': specialisation,
        'email': email,
        'phone': phone,
        'address': address,
        'created_at': created_at,
        'updated_at': updated_at,
    })

@doctor_login_required
def edit_password(request):
    return render(request, 'doctor/edit_password.html')

@doctor_login_required
def doctor_dashboard(request):
    doctor = request.doctor
    today = timezone.now()

    # Today date
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    # Today Appointments
    today_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointed_datetime__range=[today_start, today_end]
    ).order_by('appointed_datetime')

    # Upcoming and past appointments
    upcoming_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointed_datetime__gte=today,
        status__in=['pending', 'confirmed']
    ).order_by('appointed_datetime')

    past_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointed_datetime__lt=today
    ).order_by('-appointed_datetime')

    # Consultations (his patients)
    consultations = Consultation.objects.filter(
        doctor=doctor
    ).select_related('appointment__patient').order_by('-created_at')

    # Group prescriptions under each consultation
    for c in consultations:
        c.prescriptions = Prescription.objects.filter(consultation=c)

    return render(request, 'doctor/doctor_dashboard.html', {
        'today_appointments': today_appointments,
        'doctor': doctor,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'consultations': consultations,
    })

@doctor_login_required
def doctor_search(request):
    doctor = request.doctor

    search_type = request.GET.get("search_type", "")
    search_date = request.GET.get("search_date", "")
    search_name = request.GET.get("search_name", "")
    search_id = request.GET.get("search_id", "")

    results = None
    results_template = ""

    # -----------------------------
    # 1. APPOINTMENT SEARCH
    # -----------------------------
    if search_type == "appointment":
        qs = Appointment.objects.filter(doctor=doctor)

        if search_date:
            qs = qs.filter(appointed_datetime__date=search_date)

        if search_name:
            qs = qs.filter(
                Q(patient__fname__icontains=search_name) |
                Q(patient__lname__icontains=search_name)
            )

        if search_id:
            qs = qs.filter(id=search_id)

        results = qs.order_by("-appointed_datetime")
        results_template = "doctor/search_results/appointments.html"

    # -----------------------------
    # 2. CONSULTATION SEARCH
    # -----------------------------
    elif search_type == "consultation":
        qs = Consultation.objects.filter(doctor=doctor)

        if search_date:
            qs = qs.filter(created_at__date=search_date)

        if search_name:
            qs = qs.filter(
                Q(appointment__patient__fname__icontains=search_name) |
                Q(appointment__patient__lname__icontains=search_name)
            )

        if search_id:
            qs = qs.filter(id=search_id)

        results = qs.order_by("-created_at")
        results_template = "doctor/search_results/consultations.html"

    # -----------------------------
    # 3. TRIAGE SEARCH (FIXED!)
    # -----------------------------
    elif search_type == "triage":
        # FIXED: triage belongs to doctor through appointment
        qs = Triage.objects.filter(appointment__doctor=doctor)

        if search_date:
            qs = qs.filter(created_at__date=search_date)

        if search_name:
            qs = qs.filter(
                Q(patient__fname__icontains=search_name) |
                Q(patient__lname__icontains=search_name) |
                Q(nurse__fname__icontains=search_name) |
                Q(nurse__lname__icontains=search_name)
            )

        if search_id:
            qs = qs.filter(id=search_id)

        results = qs.order_by("-created_at")
        results_template = "doctor/search_results/triage.html"

    # -----------------------------
    # 4. MEDICAL RECORD SEARCH
    # -----------------------------
    elif search_type == "medical_record":
        qs = Consultation.objects.filter(doctor=doctor)

        if search_date:
            qs = qs.filter(created_at__date=search_date)

        if search_name:
            qs = qs.filter(
                Q(appointment__patient__fname__icontains=search_name) |
                Q(appointment__patient__lname__icontains=search_name)
            )

        if search_id:
            qs = qs.filter(id=search_id)

        # Attach triage
        for c in qs:
            c.triage = Triage.objects.filter(appointment=c.appointment).first()

        results = qs.order_by("-created_at")
        results_template = "doctor/search_results/medical_records.html"

    # -----------------------------
    # 5. PRESCRIPTION SEARCH
    # -----------------------------
    elif search_type == "prescription":
        qs = Prescription.objects.filter(consultation__doctor=doctor)

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
        results_template = "doctor/search_results/prescriptions.html"

    return render(request, "doctor/doctor_search.html", {
        "doctor": doctor,
        "results": results,
        "results_template": results_template,
        "search_type": search_type,
        "search_date": search_date,
        "search_name": search_name,
        "search_id": search_id,
    })
