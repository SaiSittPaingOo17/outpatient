from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect 
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

from .models import Patient
from .forms import PatientForm

# decorators.py from appointment-app
from appointment.decorators import patient_login_required

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

# display profile information
@patient_login_required
def patient_profile(request):
    patient_id = request.session.get('patient_id')
    patient = get_object_or_404(Patient, id=patient_id)

    fname = patient.fname
    lname = patient.lname
    date_of_birth = patient.date_of_birth
    gender = patient.gender
    marital_status = patient.marital_status
    phone = patient.phone
    email = patient.email
    address = patient.address
    created_at = patient.created_at
    updated_at = patient.updated_at


    return render(request, 'patient/patient_profile.html',{
        'fname': fname,
        'lname': lname,
        'date_of_birth': date_of_birth,
        'gender': gender,
        'marital_status': marital_status,
        'phone': phone,
        'email': email,
        'address': address,
        'created_at': created_at,
        'updated_at': updated_at,
    })

# edit profile information
@patient_login_required
def edit_profile(request):
    patient_id = request.session.get('patient_id')
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        title = request.POST.get('title','')
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        gender = request.POST.get('gender', '')
        marital_status = request.POST.get('marital_status', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        password = request.POST.get('password', '')

        patient.title = title
        patient.fname = fname
        patient.lname = lname
        patient.date_of_birth = date_of_birth
        patient.gender = gender
        patient.marital_status = marital_status
        patient.phone = phone
        patient.address = address

        if password.strip():
            patient.password = make_password(password)

        patient.save()

        messages.success(request, "Your profile has been updated successfully.")
        return HttpResponseRedirect(reverse('patient:patient_profile'))

    else:
        title = patient.title
        fname = patient.fname
        lname = patient.lname
        date_of_birth = patient.date_of_birth
        gender = patient.gender
        marital_status = patient.marital_status
        phone = patient.phone
        email = patient.email
        address = patient.address
        created_at = patient.created_at
        updated_at = patient.updated_at

    return render(request, 'patient/edit_profile.html',{
        'title': title,
        'fname': fname,
        'lname': lname,
        'date_of_birth': date_of_birth,
        'gender': gender,
        'marital_status': marital_status,
        'phone': phone,
        'email': email,
        'address': address,
        'created_at': created_at,
        'updated_at': updated_at,
    })
    