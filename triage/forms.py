from django import forms
from .models import Triage


class TriageForm(forms.ModelForm):
    class Meta:
        model = Triage
        fields = [
            'appointment',
            'patient',
            'nurse',
            'department',
            'temperature',
            'pulse_rate',
            'resp_rate',
            'oxygen_saturation',
            'systolic_pressure',
            'diastolic_pressure',
            'weight',
            'height',
            'blood_sugar',
            'allergies',
            'last_menstrual_period',
            'note',
            'status',
        ]
        exclude = ['appointment', 'nurse', 'patient', 'department', 'status']
        # widgets = {
        #     'chief_complaint': forms.Textarea(attrs={'rows': 2}),
        #     'nurse_notes': forms.Textarea(attrs={'rows': 3}),
        # }
        
