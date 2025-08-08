from django.utils import timezone
from .models import Appointment

def update_due_appointments():
    now = timezone.now()
    due_appointments = Appointment.objects.filter(
        status__in=['pending', 'confirmed'],
        appointed_datetime__lt=now
    )
    due_appointments.update(status='due')
