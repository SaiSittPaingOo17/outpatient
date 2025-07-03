from django.shortcuts import render
from django.http import HttpResponseRedirect 
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

from .models import Patient
from .forms import PatientForm

# Register
def patient_register(request):
    if request.method == 'POST':
        # print('Post Data', request.POST)
        form = PatientForm(request.POST)
        if form.is_valid():
            # print('Form Validataion: ',form.is_valid)
            # if not form.is_valid():
                # print('Form Error: ',form.errors)
            form.instance.password = make_password(form.cleaned_data['password'])
            form.save()
            messages.success(request, "Registration is successfully completed.")
            return HttpResponseRedirect(reverse('patient:index'))
        else:
            fname = request.POST['fname']
            lname = request.POST['lname']
            date_of_birth = request.POST['date_of_birth']
            gender = request.POST['gender']
            phone = request.POST['phone']
            address = request.POST['address']
            messages.error(request, ('Invalid Form Input ! Please try again.'))
            
            return render(request,'patient/patient_register.html',{
                'fname': fname,
                'lname': lname,
                'date_of_birth': date_of_birth,
                'gender': gender,
                'phone': phone,
                'address': address
            })
        
    else:
        return render(request, 'patient/patient_register.html') 

# Login
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
                return HttpResponseRedirect(reverse('appointment:search_doctors'))
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