from django.db import models

class Fee(models.Model):
    FEE_TYPES = [
        ('consultation', 'Consultation'),
        ('lab_test', 'Laboratory Test'),
        ('medication', 'Medication'),
    ]

    fee_type = models.CharField(max_length=20, choices=FEE_TYPES)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.amount} Ks"
