from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ValidationError

from django.utils import timezone
from datetime import timedelta, datetime

from .models import DoctorAvailability, Appointment
from doctor.models import Doctor, Department
from patient.models import Patient
from .forms import AppointmentForm
from .decorators import doctor_login_required, patient_login_required


def index(request):
    return render(request,'appointment/index.html')
# -----------------------------
# Doctor Views
# -----------------------------
@doctor_login_required
def doctor_availability_view(request):
    doctor = request.doctor
    availability = DoctorAvailability.objects.filter(doctor=doctor)
    return render(request, 'appointment/doctor_availability.html', {
        'availability': availability,
        'doctor': doctor
    })

@doctor_login_required
def add_availability(request):
    doctor = request.doctor
    if request.method == 'POST':
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        try:
            availability = DoctorAvailability(
                doctor=doctor,
                available_date=date,
                start_time=start_time,
                end_time=end_time
            )
            # Clean method to validate times
            availability.full_clean()
            availability.save()
            
            messages.success(request, f'Availability added for {date} from {start_time} to {end_time}.')
            return redirect('appointment:availability')
            
        except ValidationError as e:
            messages.error(request, f'Error: {e.message_dict.get("__all__", ["Invalid time range"])[0]}')
        except Exception as e:
            messages.error(request, f'Error adding availability: {str(e)}')
    return render(request, 'appointment/add_availability.html',{
        'doctor':doctor,
        
    })

@doctor_login_required
def doctor_appointments(request):
    doctor = request.doctor
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-created_at')
    return render(request, 'appointment/doctor_appointments.html', {
        'appointments': appointments,
        'doctor': doctor,
    })

@doctor_login_required
def confirm_appointment(request, appointment_id):
    doctor = request.doctor
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    if appointment.status == 'pending':
        appointment.status = 'confirmed'
        appointment.save()
        messages.success(request, 'Appointment confirmed.')
    return redirect('appointment:doctor_appointments')


# -----------------------------
# Patient Views
# -----------------------------
@patient_login_required
def search_doctors(request):
    query = request.GET.get('q')  # Name search
    department = request.GET.get('department')  # Department search
    
    # All active doctors
    doctors = Doctor.objects.filter(status='active').select_related('department')
    
    # Filter by name
    if query:
        doctors = doctors.filter(fname__icontains=query)
    
    # Filter by department nam
    if department:
        doctors = doctors.filter(department__dep_name__icontains=department)
    
    # Get all active departments
    all_departments = Department.objects.filter(status='active').values_list('dep_name', flat=True).distinct().order_by('dep_name')
    
    return render(request, 'appointment/search_doctors.html', {
        'doctors': doctors,
        'all_departments': all_departments,
        'selected_department': department,
        'search_query': query
    })

# @patient_login_required
# def view_availability(request, doctor_id):
#     doctor = get_object_or_404(Doctor, id=doctor_id)
#     available_slots = DoctorAvailability.objects.filter(doctor=doctor)
#     return render(request, 'appointment/view_availability.html', {
#         'doctor': doctor,
#         'available_slots': available_slots
#     })

@patient_login_required
def patient_view_availability(request, doctor_id):
    doctor_info = get_object_or_404(Doctor, id=doctor_id, status='active')
    
    # Get available slots for this doctor
    available_slots = DoctorAvailability.objects.filter(
        doctor=doctor_info,
        available_date__gte=timezone.now().date()
    ).order_by('available_date', 'start_time')
    
    # Get patient info from session
    patient_id = request.session.get('patient_id')
    patient = get_object_or_404(Patient, id=patient_id)
    
    return render(request, 'appointment/patient_view_availability.html', {
        'doctor_info': doctor_info,
        'available_slots': available_slots,
        'patient': patient  # Only pass patient context
    })

@patient_login_required
def book_appointment(request, availability_id):
    availability = get_object_or_404(DoctorAvailability, id=availability_id)
    patient_id = request.session.get('patient_id')
    patient = get_object_or_404(Patient, id=patient_id)

    # appointment_datetime = timezone.make_aware(
    #     datetime.combine(availability.available_date, availability.start_time, availability.end_time)
    # )
    if timezone.now() + timedelta(days=2) > timezone.make_aware(datetime.combine(availability.available_date, availability.start_time)):
        messages.error(request, 'You must book at least 2 days in advance.')
        return redirect('view_availability', doctor_id=availability.doctor.id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.doctor = availability.doctor
            appointment.appointed_datetime = timezone.make_aware(datetime.combine(availability.available_date, availability.start_time))
            appointment.status = 'pending'
            appointment.save()
            messages.success(request, 'Appointment request sent.')
            return HttpResponseRedirect(reverse('appointment:search_doctors'))
    else:
        form = AppointmentForm()

    return render(request, 'appointment/book_appointment.html', {
        'form': form,
        'availability': availability
    })

@patient_login_required
def view_appointments(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        messages.error(request, "You must be logged in to view your appointments.")
        return redirect('patient:patient_login')

    appointments = Appointment.objects.filter(patient_id=patient_id).order_by('-appointed_datetime')

    return render(request, 'appointment/view_appointments.html', {
        'appointments': appointments
    })