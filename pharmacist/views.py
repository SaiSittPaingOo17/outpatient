from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Pharmacist
from .decorators import pharmacist_login_required

from django.contrib import messages
from django.contrib.auth.hashers import check_password

from consultation.models import Prescription, PrescriptionType
from payment.models import Payment

def pharmacist_home_redirect(request):
    return redirect('pharmacist:pharmacist_dashboard')

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

    med_type = PrescriptionType.objects.get(prescription_type='medication')

    medications = Prescription.objects.filter(prescription_type=med_type)

    # Pre-calc completion stats for each consultation
    consult_stats = {}

    for med in medications:
        cons = med.consultation

        if cons.id not in consult_stats:
            total = cons.prescription_set.count()
            completed = cons.prescription_set.filter(status='completed').count()

            consult_stats[cons.id] = {
            "total": total,
            "completed": completed,
            "done": (total == completed and total > 0),
            "payment_id": getattr(cons, "payment", None).id if hasattr(cons, "payment") else None
        }
        
        

    return render(request, 'pharmacist/show_medications.html', {
        'pharmacist': pharmacist,
        'medications': medications,
        'consult_stats': consult_stats,
    })


@pharmacist_login_required
def update_status(request, prescription_id):
    pharmacist = request.pharmacist
    prescription = get_object_or_404(Prescription, id=prescription_id)

    if request.method == "POST":
        status = request.POST.get("status")
        prescription.status = status
        prescription.save()

        consultation = prescription.consultation

        payment, created = Payment.objects.get_or_create(
            consultation=consultation,
            defaults={
                'patient': consultation.appointment.patient,
                'appointment': consultation.appointment,
                'total_amount': 0,
                'amount_paid': 0,
                'status': 'unpaid'
            }
        )

        if status == "completed":
            return HttpResponseRedirect(reverse('payment:make_payment', args=[payment.id]))

        return HttpResponseRedirect(reverse('pharmacist:show_medications'))

    return render(request, 'pharmacist/update_status.html', {
        'pharmacist': pharmacist,
        'prescription': prescription,
    })

@pharmacist_login_required
def pharmacist_dashboard(request):
    pharmacist = request.pharmacist

    # Fetch prescriptions(medication only)
    med_type = PrescriptionType.objects.get(prescription_type='medication')
    prescriptions = Prescription.objects.filter(prescription_type=med_type)

    # Stats
    total_prescriptions = prescriptions.count()
    pending_prescriptions = prescriptions.filter(status='pending').count()
    processing_prescriptions = prescriptions.filter(status='processing').count()
    completed_prescriptions = prescriptions.filter(status='completed').count()

    # Payment stats — linked through consultation
    payments = Payment.objects.all()
    payments_created = payments.count()
    payments_paid = payments.filter(status='paid').count()

    return render(request, 'pharmacist/pharmacist_dashboard.html', {
        'pharmacist': pharmacist,

        'total_prescriptions': total_prescriptions,
        'pending_prescriptions': pending_prescriptions,
        'processing_prescriptions': processing_prescriptions,
        'completed_prescriptions': completed_prescriptions,

        'payments_created': payments_created,
        'payments_paid': payments_paid,
    })

from django.db.models import Q
from consultation.models import Prescription, PrescriptionType
from payment.models import Payment


@pharmacist_login_required
def pharmacist_search(request):
    pharmacist = request.pharmacist

    search_type = request.GET.get("search_type", "").strip()
    raw_date = request.GET.get("search_date", "").strip()
    search_date = raw_date if raw_date else None
    search_name = request.GET.get("search_name", "").strip()
    search_id = request.GET.get("search_id", "").strip()

    results = None
    results_template = ""

    # -----------------------------
    # 1. Medication Search
    # -----------------------------
    if search_type == "medication":
        med_type = PrescriptionType.objects.get(prescription_type='medication')
        qs = Prescription.objects.filter(prescription_type=med_type)

        if search_date:
            qs = qs.filter(created_at__date=search_date)

        if search_name:
            qs = qs.filter(
                Q(consultation__appointment__patient__fname__icontains=search_name) |
                Q(consultation__appointment__patient__lname__icontains=search_name)
            )

        if search_id:
            qs = qs.filter(id=search_id)

        results = qs.order_by('-created_at')
        results_template = "pharmacist/search_results/medications.html"

    # -----------------------------
    # 2. Payment Search
    # -----------------------------
    elif search_type == "payment":
        qs = Payment.objects.all()

        if search_date:
            qs = qs.filter(created_at__date=search_date)

        if search_name:
            qs = qs.filter(
                Q(patient__fname__icontains=search_name) |
                Q(patient__lname__icontains=search_name)
            )

        if search_id:
            qs = qs.filter(id=search_id)

        results = qs.order_by('-created_at')
        results_template = "pharmacist/search_results/payments.html"

    return render(request, "pharmacist/pharmacist_search.html", {
        "pharmacist": pharmacist,
        "results": results,
        "results_template": results_template,
        "search_type": search_type,
        "search_date": search_date,
        "search_name": search_name,
        "search_id": search_id,
    })
