from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from appointment.decorators import doctor_login_required
from triage.models import Triage
from appointment.models import Appointment
from .models import Consultation
from .models import PrescriptionType
from .models import Prescription

from .forms import ConsultationForm
from django.contrib import messages

@doctor_login_required
def index(request):
    return render(request, 'consultation/index.html')

@doctor_login_required
def show_triage(request):
    doctor = request.doctor

    # Get all appointments of the doctor 
    appointment  = Appointment.objects.filter(doctor=doctor)

    # Retrieve triage records linked to appointments
    triage_records = Triage.objects.filter(appointment__in=appointment).select_related('patient', 'appointment')
    print(triage_records)
    return render(request, 'consultation/show_triage.html', {
        'triage_records': triage_records,
        'doctor': doctor,
    })

@doctor_login_required
def record(request, triage_id):
    doctor = request.doctor
    # appointment = Appointment.objects.get(id=doctor.id)
    triage = Triage.objects.get(id=triage_id)
    appointment = triage.appointment

    # check the consultation already exists to prevent duplication
    existing_consultation = Consultation.objects.filter(
        appointment=appointment,
        doctor=doctor
    ).first()

    if existing_consultation:
        messages.warning(request, "Consultation already exists for this appointment.")
        return redirect('consultation:show_triage')  # redirect instead of showing the form again

    if request.method == "POST":
        
        form = ConsultationForm(request.POST)

        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.doctor = doctor
            consultation.appointment = appointment
            print(request.POST)
            form.save()
            messages.success(request, 'Consultation is finished.')
        
        else:
            chief_comp = request.POST['chief_comp']
            present_ill = request.POST['present_ill']
            past_med = request.POST['past_med']
            past_sur = request.POST['past_sur']
            medica_his = request.POST['medica_his']
            og_his = request.POST['og_his']
            fam_his = request.POST['fam_his']
            soc_his = request.POST['soc_his']
            phy_exam = request.POST['phy_exam']
            diag = request.POST['diag']
            notes = request.POST['notes']

            messages.warning(request, 'Please fill the form completely')
            return render(request, 'consultation/record.html',{
                'chief_comp': chief_comp,
                'present_ill': present_ill,
                'past_med': past_med,
                'past_sur': past_sur,
                'medica_his': medica_his,
                'og_his': og_his,
                'fam_his': fam_his,
                'soc_his': soc_his,
                'phy_exam': phy_exam,
                'diag': diag,
                'notes': notes,
            })   
    else:
        form = ConsultationForm()

    return render(request, 'consultation/record.html',{
        'triage': triage,
        'doctor': doctor,
        'appointment': appointment,
        'form': form,
    })

@doctor_login_required
def show_consultation(request):
    doctor = request.doctor

    #double underscore: 
    # To access the Patient model (which is linked through the Appointment model), you must use double underscores (__), not an underscore.
    consultations = Consultation.objects.filter(doctor=doctor).select_related('appointment__patient', 'doctor')

    return render(request, 'consultation/show_consultation.html',{
        'doctor': doctor,
        'consultations': consultations,
    })

@doctor_login_required
def edit_consultation(request, consultation_id):
    consultation = Consultation.objects.get(id=consultation_id)
    appointment = consultation.appointment
    doctor = request.doctor

    if request.method == 'POST':
        form = ConsultationForm(request.POST, instance=consultation)

        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.doctor = doctor
            consultation.appointment = appointment
            # print(request.POST)
            consultation.save()
            messages.success(request,'Consultation is updated.')
            return HttpResponseRedirect(reverse('consultation:show_consultation'))
        else:
            chief_comp = request.POST['chief_comp']
            present_ill = request.POST['present_ill']
            past_med = request.POST['past_med']
            past_sur = request.POST['past_sur']
            medica_his = request.POST['medica_his']
            og_his = request.POST['og_his']
            fam_his = request.POST['fam_his']
            soc_his = request.POST['soc_his']
            phy_exam = request.POST['phy_exam']
            diag = request.POST['diag']
            notes = request.POST['notes']

            messages.warning(request, 'Please fill the form completely')
            return render(request, 'consultation/edit_consultation.html',{
                'chief_comp': chief_comp,
                'present_ill': present_ill,
                'past_med': past_med,
                'past_sur': past_sur,
                'medica_his': medica_his,
                'og_his': og_his,
                'fam_his': fam_his,
                'soc_his': soc_his,
                'phy_exam': phy_exam,
                'diag': diag,
                'notes': notes,
            })   
    else:
        form = ConsultationForm(instance=consultation)

    return render(request, 'consultation/edit_consultation.html', {
    'doctor': doctor,
    'consultation': consultation,
    'appointment': appointment,
    'form': form,
    })

@doctor_login_required
def make_prescription(request, consultation_id):
    doctor = request.doctor
    consultation = Consultation.objects.get(id=consultation_id)
    appointment = consultation.appointment

    if request.method == 'POST':
        lab_text = request.POST.get('lab_prescri')
        med_text = request.POST.get('med_prescri')

        # Prescription types
        lab_type = PrescriptionType.objects.get(prescription_type='laboratory')
        med_type = PrescriptionType.objects.get(prescription_type='medication')

        # laboratory prescription if provided
        if lab_text and lab_text.strip() != "":
            Prescription.objects.create(
                prescription_type=lab_type,
                consultation=consultation,
                prescription=lab_text.strip()
            )

        # medication prescription if provided
        if med_text and med_text.strip() != "":
            Prescription.objects.create(
                prescription_type=med_type,
                consultation=consultation,
                prescription=med_text.strip()
            )

        return redirect('consultation:view_prescription', consultation_id=consultation.id)

    return render(request, 'consultation/make_prescription.html', {
        'doctor': doctor,
        'consultation': consultation,
        'appointment': appointment,
    })

@doctor_login_required
def view_prescription(request, consultation_id):
    consultation = Consultation.objects.get(id=consultation_id)
    prescriptions = Prescription.objects.filter(consultation=consultation)

    return render(request, 'consultation/view_prescription.html', {
        'consultation': consultation,
        'prescriptions': prescriptions
    })

@doctor_login_required
def edit_prescription(request, prescription_id):
    prescription = Prescription.objects.get(id=prescription_id)
    consultation = prescription.consultation

    if request.method == "POST":
        new_text = request.POST.get("prescription")

        # Update and save
        prescription.prescription = new_text
        prescription.save()

        messages.success(request, "Prescription updated successfully!")
        return redirect('consultation:view_prescription', consultation_id=consultation.id)

    return render(request, 'consultation/edit_prescription.html', {
        'prescription': prescription,
        'consultation': consultation,
    })

@doctor_login_required
def delete_prescription(request, prescription_id):
    prescription = Prescription.objects.get(id=prescription_id)
    consultation_id = prescription.consultation.id
    prescription.delete()

    messages.success(request, "Prescription deleted successfully.")
    return redirect('consultation:view_prescription', consultation_id=consultation_id)

