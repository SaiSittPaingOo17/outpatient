from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from appointment.models import Appointment
from nurse.models import Nurse
from patient.models import Patient
from doctor.models import Department

class Triage(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('due', 'Due'),
    ]

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    temperature = models.FloatField(
        validators=[MinValueValidator(25), MaxValueValidator(45)],
        help_text="Body temperature in °C"
    )
    pulse_rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(300)],
        help_text="Beats per minute"
    )
    resp_rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(80)],
        help_text="Breaths per minute"
    )
    oxygen_saturation = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True,
        help_text="SpO₂ percentage"
    )
    systolic_pressure = models.IntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(300)]
    )
    diastolic_pressure = models.IntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(200)]
    )
    weight = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(500)],
        help_text="Weight in kilograms"
    )
    height = models.FloatField(
        validators=[MinValueValidator(0.3), MaxValueValidator(3)],
        help_text="Height in meters"
    )

    blood_sugar = models.FloatField(null=True, blank=True)
    allergies = models.CharField(max_length=128, null=True, blank=True)
    last_menstrual_period = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def bmi(self):
        if self.height and self.height > 0:
            return round(self.weight / (self.height ** 2), 2)
        return None

    def __str__(self):
        return f"Triage Record {self.id} - {self.created_at.strftime('%Y-%m-%d')}"
