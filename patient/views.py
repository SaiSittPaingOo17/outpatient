from django.shortcuts import render
from django.http import HttpResponseRedirect 
from django.urls import reverse

from django.contrib import messages

from .models import Patient
from .forms import PatientForm

def index(request):
    return render(request, 'patient/index.html')

def patient_register(request):
    if request.method == 'POST':
        # print('Post Data', request.POST)
        form = PatientForm(request.POST or None)
        if form.is_valid():
            # print('Form Validataion: ',form.is_valid)
            # if not form.is_valid():
                # print('Form Error: ',form.errors)
            form.save()
            messages.success(request, "Registration is successfully completed.")
            return HttpResponseRedirect(reverse('index'))
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

def patient_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        check_user = Patient.object.get(email)
        if check_user:
            check_password = Patient.object.get()
            if check_password == password:
                messages.success("Login Success")
                return HttpResponseRedirect(reverse('patient:index'))
            else:
                message = messages.danger("Wrong email or password! Please try again")
                return render(request, 'patient/patient_login.html',{
                    'message': message
                })


     

def patient_logout(request):
    return render(request, 'patient/patient_logout')