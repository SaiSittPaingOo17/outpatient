from django.db import models

# Create your models here.
class Doctor(models.Model):
    doc_name = models.CharField(max_length=64)
    doc_dep = models.CharField(max_length=64)

    def __str__(self):
        return f"Dr. {self.doc_name} ({self.doc_dep})"

class Department(models.Model):
    dep_name = models.CharField(max_length=64)
    doctors = models.ManyToManyField(Doctor, blank=True, related_name='specialists')

    def __str__(self):
        return f"{self.dep_name}"


class Patient(models.Model):
    pat_name = models.CharField(max_length=64)
    pat_phone = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.pat_name} ({self.pat_phone})"

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    apt_time = models.DateTimeField()

    def __str__(self):
        return f"{self.apt_time} : {self.patient} with {self.doctor}"