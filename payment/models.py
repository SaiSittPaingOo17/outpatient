from django.db import models
from datetime import datetime
from patient.models import Patient
from appointment.models import Appointment
from consultation.models import Consultation, Prescription
from billing.models import Fee   

class Payment(models.Model):

    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Debit/Credit Card'),
        ('mobile_banking', 'Mobile Banking (KBZPay, WavePay)'),
        ('wallet', 'E-Wallet'),
        ('bank_transfer', 'Bank Transfer'),
        ('insurance', 'Insurance'),
    ]

    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE)

    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medication_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    test_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_method = models.CharField(
        max_length=30, choices=PAYMENT_METHODS, blank=True, null=True
    )

    status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS, default='unpaid'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def manual_recalculate_total(self):
        self.total_amount = (
            (self.consultation_fee or 0)
            + (self.medication_fee or 0)
            + (self.test_fee or 0)
        )
        self.save()

    # calculate total from consultation + prescriptions
    def calculate_total(self):
        total = 0

        # Consultation Fee
        consultation_fee = Fee.objects.filter(fee_type='consultation').first()
        if consultation_fee:
            total += consultation_fee.amount

        # Completed Medication Prescriptions
        medication_prescriptions = Prescription.objects.filter(
            consultation=self.consultation,
            prescription_type__prescription_type='medication',
            status='completed'
        )

        for presc in medication_prescriptions:
            med_fee = Fee.objects.filter(fee_type='medication', name=presc.prescription).first()
            if med_fee:
                total += med_fee.amount

        # Completed Lab Test Prescriptions
        lab_prescriptions = Prescription.objects.filter(
            consultation=self.consultation,
            prescription_type__prescription_type='laboratory',
            status='completed'
        )

        for lab in lab_prescriptions:
            lab_fee = Fee.objects.filter(fee_type='lab_test', name=lab.prescription).first()
            if lab_fee:
                total += lab_fee.amount

        self.total_amount = total
        self.save()

    def __str__(self):
        return f"Payment #{self.id} - {self.patient.fname} {self.patient.lname}"

def all_prescriptions_completed(self):
    prescriptions = self.consultation.prescription_set.all()
    return all(p.status == "completed" for p in prescriptions)