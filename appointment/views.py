from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
# datetime
from django.utils import timezone
from datetime import timedelta, datetime, date as date_func
# databases
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
        'doctor': doctor,
        
    })

@doctor_login_required
def add_availability(request):
    doctor = request.doctor
    if request.method == 'POST':
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        # Check if availability already exists
        existing = DoctorAvailability.objects.filter(
            doctor=doctor,
            available_date=date,
            start_time=start_time,
            end_time=end_time
        ).exists()
        
        if existing:
            messages.error(request, 'This availability slot already exists.')
            return render(request, 'appointment/add_availability.html', {'doctor': doctor})
        
        # Convert string date to date object
        availability_date = datetime.strptime(date, '%Y-%m-%d').date()
        today = date_func.today()
        min_date = today + timedelta(days=2)
        
        # ensure availability is made prior
        if availability_date < min_date:
            messages.error(request, 'Availability must be scheduled at least 2 days in advance.')
            return render(request, 'appointment/add_availability.html', {'doctor': doctor})
        
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
            return HttpResponseRedirect(reverse('appointment:availability'))
            
        except ValidationError as e:
            messages.error(request, f'Error: {e.message_dict.get("__all__", ["Invalid time range"])[0]}')
        except IntegrityError:
            messages.error(request, 'Invalid schedule')
        except Exception as e:
            messages.error(request, f'Error adding availability: {str(e)}')
    
    return render(request, 'appointment/add_availability.html', {
        'doctor': doctor,
    })

@doctor_login_required
def delete_availability(request, availability_id):
    doctor = request.doctor
    availability = get_object_or_404(DoctorAvailability, id=availability_id, doctor=doctor)
    
    # Check if there are any pending/confirmed appointments for this slot
    has_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointed_datetime__date=availability.available_date,
        appointed_datetime__time__gte=availability.start_time,
        appointed_datetime__time__lt=availability.end_time,
        status__in=['pending', 'confirmed']
    ).exists()
    
    if has_appointments:
        messages.error(request, 'Cannot delete availability slot that has existing appointments.')
    else:
        availability.delete()
        messages.success(request, f'Availability for {availability.available_date} from {availability.start_time} to {availability.end_time} has been deleted.')
    
    return HttpResponseRedirect(reverse('appointment:availability'))

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
    return HttpResponseRedirect(reverse('appointment:doctor_appointments'))

@doctor_login_required
def cancel_appointment_doctor(request, appointment_id):
    doctor = request.doctor
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    
    if request.method == 'POST':
        if appointment.status in ['pending', 'confirmed']:
            appointment.status = 'cancelled'
            appointment.cancelled_by = 'doctor'
            appointment.cancellation_reason = request.POST.get('reason', '')
            appointment.save()
            messages.success(request, 'Appointment cancelled successfully.')
        else:
            messages.error(request, 'Cannot cancel this appointment.')
    
    return HttpResponseRedirect(reverse('appointment:doctor_appointments'))

# -----------------------------
# Patient Views
# -----------------------------
@patient_login_required
def search_doctors(request):
    query = request.GET.get('q')  # Name search
    department = request.GET.get('department')  # Department search
    
    # Get patient info from session
    patient_id = request.session.get('patient_id')
    patient = get_object_or_404(Patient, id=patient_id)
    
    # All active doctors
    doctors = Doctor.objects.filter(status='active').select_related('department')
    
    # Filter by name
    if query:
        doctors = doctors.filter(fname__icontains=query)
    
    # Filter by department name
    if department:
        doctors = doctors.filter(department__dep_name__icontains=department)
    
    # Get all active departments
    all_departments = Department.objects.filter(status='active').values_list('dep_name', flat=True).distinct().order_by('dep_name')
    
    return render(request, 'appointment/search_doctors.html', {
        'doctors': doctors,
        'all_departments': all_departments,
        'selected_department': department,
        'search_query': query,
        'patient': patient
    })

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
        'patient': patient
    })

@patient_login_required
def book_appointment(request, availability_id):
    availability = get_object_or_404(DoctorAvailability, id=availability_id)
    patient_id = request.session.get('patient_id')
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Calculate appointment datetime 
    appointment_datetime = timezone.make_aware(datetime.combine(availability.available_date, availability.start_time))
    
    # Check if booking is at least 2 days in advance
    if timezone.now() + timedelta(days=2) > appointment_datetime:
        messages.error(request, 'You must book at least 2 days in advance.')
        return redirect('appointment:patient_view_availability', doctor_id=availability.doctor.id)
    
    # Check for overlapping appointments - FIXED: Now actually using the result
    overlapping_appointments = Appointment.objects.filter(
        patient=patient,
        doctor=availability.doctor,
        appointed_datetime__date=availability.available_date,
        appointed_datetime__time__range=(availability.start_time, availability.end_time),
        status__in=['pending', 'confirmed']
    ).exists()
    
    if overlapping_appointments:
        messages.error(request, 'You already have an overlapping appointment with this doctor.')
        return redirect('appointment:patient_view_availability', doctor_id=availability.doctor.id)
    
    # Check if patient already has an appointment for this exact time slot
    existing_appointment = Appointment.objects.filter(
        patient=patient,
        doctor=availability.doctor,
        appointed_datetime=appointment_datetime,
        status__in=['pending', 'confirmed']
    ).exists()
    
    if existing_appointment:
        messages.error(request, 'You already have an appointment booked for this time slot.')
        return redirect('appointment:patient_view_availability', doctor_id=availability.doctor.id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Double-check for race conditions
            existing_appointment = Appointment.objects.filter(
                patient=patient,
                doctor=availability.doctor,
                appointed_datetime=appointment_datetime,
                status__in=['pending', 'confirmed']
            ).exists()
            
            if existing_appointment:
                messages.error(request, 'You already have an appointment booked for this time slot.')
                return redirect('appointment:patient_view_availability', doctor_id=availability.doctor.id)
            
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.doctor = availability.doctor
            appointment.appointed_datetime = appointment_datetime
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
    patient = get_object_or_404(Patient, id=patient_id)
    
    if not patient_id:
        messages.error(request, "You must be logged in to view your appointments.")
        return HttpResponseRedirect(reverse('patient:patient_login'))
    
    appointments = Appointment.objects.filter(patient_id=patient_id).order_by('-appointed_datetime')
    
    return render(request, 'appointment/view_appointments.html', {
        'appointments': appointments,
        'patient': patient,
    })

@patient_login_required
def cancel_appointment(request, appointment_id):
    patient_id = request.session.get('patient_id')
    patient = get_object_or_404(Patient, id=patient_id)
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)
    
    if not appointment.is_cancellable():
        messages.error(request, 'Cannot cancel appointment less than 2 days in advance.')
        return redirect('appointment:view_appointments')
    
    if appointment.status not in ['pending', 'confirmed']:
        messages.error(request, 'Cannot cancel this appointment.')
        return redirect('appointment:view_appointments')
    
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.cancelled_by = 'patient'
        appointment.cancellation_reason = request.POST.get('reason', '')
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully.')
        return redirect('appointment:view_appointments')
    
    # Handle GET request - show cancellation form
    return render(request, 'appointment/cancel_appointment.html', {
        'appointment': appointment,
        'patient': patient
    })

@patient_login_required
def cancel_appointment_form(request, appointment_id):
    patient_id = request.session.get('patient_id')
    patient = get_object_or_404(Patient, id=patient_id)
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)
    
    if not appointment.is_cancellable():
        messages.error(request, 'Cannot cancel appointment less than 2 days in advance.')
        return redirect('appointment:view_appointments')
    
    if appointment.status not in ['pending', 'confirmed']:
        messages.error(request, 'Cannot cancel this appointment.')
        return redirect('appointment:view_appointments')
    
    return render(request, 'appointment/cancel_appointment.html', {
        'appointment': appointment,
        'patient': patient
    })