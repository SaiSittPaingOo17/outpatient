from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'consultation_fee',
            'medication_fee',
            'test_fee',
            'amount_paid',
            'payment_method'
        ]

