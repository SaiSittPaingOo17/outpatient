from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta, date
from appointment.models import Appointment
from doctor.models import Doctor

class Consultation(models.Model):
    STATUS_CHOICE = [
        ('active','Active'),
        ('inactive', 'Inactive'),
    ]
 
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    chief_comp = models.CharField()
    present_ill = models.TextField(blank=True, null=True)
    past_med = models.TextField(blank=True, null=True)
    past_sur = models.TextField(blank=True, null=True)
    medica_his = models.TextField(blank=True, null=True)
    og_his = models.TextField(blank=True, null=True)
    fam_his = models.TextField(blank=True, null=True)
    soc_his = models.TextField(blank=True, null=True)
    phy_exam = models.TextField(blank=True, null=True)
    diag = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICE, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Consultated by {self.doctor} at {self.created_at}"

class PrescriptionType(models.Model):
    TYPE_CHOICES = [
        ('laboratory', 'Laboratory'),
        ('medication','Medication'),
    ]
    prescription_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='medication')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Prescription Type : {self.prescription_type}'

class Prescription(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]

    prescription_type = models.ForeignKey(PrescriptionType, on_delete=models.CASCADE)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    prescription = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Precription : {self.prescription}"
