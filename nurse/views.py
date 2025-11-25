from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .decorators import nurse_login_required

from .models import Nurse
from triage.models import Triage

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.utils import timezone

def nurse_home_redirect(request):
    return redirect('nurse:nurse_dashboard')

@nurse_login_required
def nurse_dashboard(request):
    nurse = None
    nurse_id = request.session.get("nurse_id")

    if nurse_id:
        nurse = get_object_or_404(Nurse, id=nurse_id)

    # Base queryset: only triage done by this nurse
    qs = Triage.objects.filter(nurse_id=nurse_id)

    # Stats
    total_records = qs.count()
    pending_records = qs.filter(status='pending').count()
    completed_records = qs.filter(status='completed').count()
    due_records = qs.filter(status='due').count()

    # Today's records
    today = timezone.now().date()
    today_records = qs.filter(created_at__date=today).count()

    # Latest 5 records
    recent_records = qs.order_by("-created_at")[:5]

    return render(request, 'nurse/nurse_dashboard.html', {
        "nurse": nurse,
        "total_records": total_records,
        "pending_records": pending_records,
        "completed_records": completed_records,
        "due_records": due_records,
        "today_records": today_records,
        "recent_records": recent_records,
    })

# nurse authentication
def nurse_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        try:
            nurse = Nurse.objects.get(email=email)

            print("Stored password:", nurse.password)
            print("Entered password:", password)

            if check_password(password, nurse.password):
                request.session['nurse_id'] = nurse.id
                request.session['nurse_email'] = nurse.email
                messages.success(request, 'Login Succeeds!')
                return HttpResponseRedirect(reverse('triage:show_appointments'))
            else:
                messages.error(request, 'Invalid Email or Password')
                return render(request, 'nurse/nurse_login.html')

        except Nurse.DoesNotExist:
            messages.error(request, 'The user does not exist')
            return render(request, 'nurse/nurse_login.html')

        except Exception as e:
            messages.error(request, f'Error: {e}')
            return render(request, 'nurse/nurse_login.html')

    return render(request, 'nurse/nurse_login.html')

def nurse_logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return HttpResponseRedirect(reverse('nurse:nurse_login'))

#nurse search
@nurse_login_required
def nurse_search(request):
    nurse_id = request.session.get("nurse_id")
    if nurse_id:
        nurse = get_object_or_404(Nurse, id=nurse_id)

    # fields
    raw_date = request.GET.get("search_date", "").strip()
    search_date = raw_date if raw_date else None
    search_name = request.GET.get("search_name", "").strip()
    search_id = request.GET.get("search_id", "").strip()

    results = Triage.objects.filter(nurse_id=nurse_id)

    if search_date:
        results = results.filter(created_at__date=search_date)

    if search_name:
        results = results.filter(
            Q(patient__fname__icontains=search_name) |
            Q(patient__lname__icontains=search_name)
        )

    if search_id:
        results = results.filter(id=search_id)

    results = results.order_by("-created_at")

    return render(request, "nurse/nurse_search.html", {
        'nurse': nurse,
        "results": results,
        "search_date": search_date,
        "search_name": search_name,
        "search_id": search_id
    })