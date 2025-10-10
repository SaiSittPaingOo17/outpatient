from django.shortcuts import render, redirect
from appointment.decorators import doctor_login_required
from triage.models import Triage
from appointment.models import Appointment
from .models import Consultation
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