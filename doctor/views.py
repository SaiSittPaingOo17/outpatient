from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Doctor

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password

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
                return HttpResponseRedirect(reverse('doctor:dashboard'))
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

def patient_login(request):
    if request.method == 'POST':
        email = request.POST.get('email','')
        password = request.POST.get('password','')

        # print(email)
        # print(password)

        try:
            patient = Patient.objects.get(email=email)

            if check_password(password, patient.password):
                request.session['patient_id'] = patient.id
                request.session['patient_email'] = patient.email

                # print(request.session['patient_id'])
                # print(request.session['patient_email'])
                messages.success(request, ('Login Succeeds!'))
                return HttpResponseRedirect(reverse('patient:index'))
            else:
                messages.error(request, "Wrong email or password! Please try again.")
                return render(request, 'patient/patient_login.html')
        
        except Patient.DoesNotExist:
            messages.error(request, 'Wrong Email or Password!')
            return render(request, 'patient/patient_login.html')
        except Exception as e:
            messages.error(request, "An error occurred. Please try again.")
            return render(request, 'patient/patient_login.html')
    else:
        return render(request, 'patient/patient_login.html')
             
# Logout
def patient_logout(request):
    request.session.flush()  # Clears all session data
    messages.success(request, "You have been logged out.")
    return HttpResponseRedirect(reverse('patient:patient_login'))