from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Doctor

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password

# import decorators.py from appointment-app
from appointment.decorators import doctor_login_required

@doctor_login_required 
def dashboard(request):
    doctor_id = request.session.get('doctor_id')
    
    if not doctor_id: 
        messages.error(request, 'Please log in first')
        return HttpResponseRedirect(reverse('doctor:doctor_login'))
    
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        context = {'doctor': doctor}
        return render(request, 'doctor/dashboard.html', context)
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor not found')
        return HttpResponseRedirect(reverse('doctor:doctor_login'))

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