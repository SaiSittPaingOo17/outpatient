from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Doctor, Patient, Appointment, Department

# Create your views here.
def index(request):
    return render(request, 'appointments/index.html',{
        'message': 'This is home page',
        # 'doctors': Doctor.objects.all(),
        # 'patients': Patient.objects.all()
        "appointments": Appointment.objects.all(),
        "departments": Department.objects.all()
    })

def appointment(request, apt_id):
    appointment = Appointment.objects.get(pk=apt_id)
    return render(request, "appointments/appointment.html",{
        "appointment": appointment
    })

def department(request, dept_id):
    dept = Department.objects.get(pk=dept_id)
    return render(request, "appointments/department.html", {
        "dept": dept,
        "doctors": dept.doctors.all(), # assigned doctors
        "no_assign_doctors": Doctor.objects.exclude(specialists=dept).all() # not assigned doctor
    })

def assign_doctor(request, dept_id):
    if request.method == "POST":
        assign_department = Department.objects.get(pk=dept_id)
        doctors = Doctor.objects.get(pk=int(request.POST['doctor']))
        doctors.specialists.add(assign_department)
    return HttpResponseRedirect(reverse("department",args=(dept_id,)))