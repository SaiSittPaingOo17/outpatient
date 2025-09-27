from django.shortcuts import render
from appointment.models import Appointment
from .models import Triage 
from .decorators import nurse_login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .forms import TriageForm

def index(request):
    return render(request, 'triage/index.html')

@nurse_login_required
def show_appointments(request):
    nurse = request.nurse
    nurse_department = nurse.department
    
    appointments = Appointment.objects.filter(
        doctor__department=nurse_department
    ).select_related('doctor', 'patient')

    return render(request, 'triage/show_appointments.html', {
        'appointments': appointments,
        'nurse': nurse,
    })

@nurse_login_required
def fill_triage(request, appointment_id):
    nurse = request.nurse
    appointment = Appointment.objects.select_related('doctor', 'patient').get(id=appointment_id)
    
    
    # check triage form exists and is valid
    if request.method == 'POST':
        form = TriageForm(request.POST)
        # print(request.POST)   

        if form.is_valid():
            triage = form.save(commit=False)

            # Manual Inputs for those not included in Triage form
            triage.appointment = appointment
            triage.patient = appointment.patient
            triage.nurse = nurse
            triage.department = nurse.department
            triage.status = "completed"

            form.save()
            messages.success(request, "Triage Form is filled.")
            return HttpResponseRedirect(reverse('triage:show_appointments'))
        else:
            temperature = request.POST['temperature']
            pulse_rate = request.POST['pulse_rate']
            resp_rate = request.POST['resp_rate']
            oxygen_saturation = request.POST['oxygen_saturation']
            systolic_pressure = request.POST['systolic_pressure']
            diastolic_pressure = request.POST['diastolic_pressure']
            weight = request.POST['weight']
            height = request.POST['height']
            blood_sugar = request.POST['blood_sugar']
            allergies = request.POST['allergies']
            last_menstrual_period = request.POST['last_menstrual_period']
            note = request.POST['note']

            messages.warning(request, 'Please fill the form correctly and completely.')
            return render(request, 'triage/fill_triage.html', {
                "appointment": appointment,
                "nurse": nurse,
                "temperature": temperature,
                "pulse_rate": pulse_rate,
                "resp_rate": resp_rate,
                "oxygen_saturation": oxygen_saturation,
                "systolic_pressure": systolic_pressure,
                "diastolic_pressure": diastolic_pressure,
                "weight": weight,
                "height": height,
                "blood_sugar": blood_sugar,
                "allergies": allergies,
                "last_menstrual_period": last_menstrual_period,
                "note": note,
            })
    else:
        form = TriageForm

    return render(request, 'triage/fill_triage.html', {
        "form": form,
        "appointment": appointment,
        "nurse": nurse,
    })

@nurse_login_required
def log(request):
    nurse = request.nurse
    triages = Triage.objects.all()
    print(triages)

    return render(request,'triage/log.html',{
        'triages': triages,
        'nurse': nurse,
    })

@nurse_login_required
def triage_details(request, triage_id):
    triage = Triage.objects.get(id=triage_id)
    nurse = request.nurse

    return render(request, 'triage/triage_details.html', {
        'triage': triage,
        'nurse': nurse,
    })

@nurse_login_required
def edit_triage(request, triage_id):
    triage = Triage.objects.get(id=triage_id)
    nurse = request.nurse

    if request.method == 'POST':
        form = TriageForm(request.POST, instance=triage)

        if form.is_valid():
            updated_triage = form.save(commit=False)

            # Update nurse and department (just in case)
            updated_triage.nurse = nurse
            updated_triage.department = nurse.department
            updated_triage.status = "completed"
            updated_triage.save()

            messages.success(request, "Triage record updated successfully.")
            return HttpResponseRedirect(reverse('triage:triage_details', args=[triage.id]))
        else:
            # Refill submitted values manually (for UX consistency)
            temperature = request.POST['temperature']
            pulse_rate = request.POST['pulse_rate']
            resp_rate = request.POST['resp_rate']
            oxygen_saturation = request.POST['oxygen_saturation']
            systolic_pressure = request.POST['systolic_pressure']
            diastolic_pressure = request.POST['diastolic_pressure']
            weight = request.POST['weight']
            height = request.POST['height']
            blood_sugar = request.POST.get('blood_sugar', '')
            allergies = request.POST.get('allergies', '')
            last_menstrual_period = request.POST.get('last_menstrual_period', '')
            note = request.POST.get('note', '')

            messages.warning(request, 'Please fill the form correctly and completely.')
            return render(request, 'triage/edit_triage.html', {
                "triage": triage,
                "nurse": nurse,
                "temperature": temperature,
                "pulse_rate": pulse_rate,
                "resp_rate": resp_rate,
                "oxygen_saturation": oxygen_saturation,
                "systolic_pressure": systolic_pressure,
                "diastolic_pressure": diastolic_pressure,
                "weight": weight,
                "height": height,
                "blood_sugar": blood_sugar,
                "allergies": allergies,
                "last_menstrual_period": last_menstrual_period,
                "note": note,
            })

    else:
        form = TriageForm(instance=triage)

    return render(request, 'triage/edit_triage.html', {
        'triage': triage,
        'nurse': nurse,
        'form': form,
    })
