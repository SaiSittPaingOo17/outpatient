from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime, date
from doctor.models import Doctor
from patient.models import Patient
from django.core.exceptions import ValidationError


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    available_date = models.DateField()
    start_time = models.TimeField(default='09:00:00')
    end_time = models.TimeField(default='21:00:00')

    class Meta:
        unique_together = ('doctor', 'available_date', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.doctor} on {self.available_date} ({self.start_time} - {self.end_time})"

    @property
    def duration(self):
        """Calculate and return the duration of the availability slot"""
        if self.start_time and self.end_time:
            start_datetime = datetime.combine(date.today(), self.start_time)
            end_datetime = datetime.combine(date.today(), self.end_time)
            duration = end_datetime - start_datetime
            
            # Convert to hours and minutes for display
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            
            if hours > 0 and minutes > 0:
                return f"{hours}h {minutes}m"
            elif hours > 0:
                return f"{hours}h"
            elif minutes > 0:
                return f"{minutes}m"
            else:
                return "0m"
        return "N/A"

    def clean(self):
        if self.start_time and self.end_time:
            start_datetime = datetime.combine(date.today(), self.start_time)
            end_datetime = datetime.combine(date.today(), self.end_time)
            duration = end_datetime - start_datetime
            
            # Check if duration is at least 3 hours
            if duration < timedelta(hours=3):
                raise ValidationError("Each availability schedule must be at least 3 hours long.")
            
            if self.start_time >= self.end_time:
                raise ValidationError("Start time must be before end time.")


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    REASON_CHOICES = [
        ('first_time', 'First-time Visit'),
        ('follow_up', 'Follow-up'),
        ('referral', 'Referral')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointed_datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    visit_reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    cancellation_reason = models.TextField(blank=True, null=True)
    cancelled_by = models.CharField(max_length=10, blank=True, null=True)  # 'doctor' or 'patient'
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def is_cancellable(self):
        """Returns True if the appointment is more than 2 days away"""
        return self.appointed_datetime - timezone.now() > timedelta(days=2)
