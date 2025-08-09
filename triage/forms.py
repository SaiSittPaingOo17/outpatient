from django import forms
from .models import Triage


class TriageForm(forms.ModelForm):
    class Meta:
        model = Triage
        fields = [
            'appt_id',               
            'blood_pressure',        
            'heart_rate',          
            'respiratory_rate',      
            'temperature',           
            'oxygen_saturation',     
            'weight',                
            'height',                
            'bmi',                   
            'chief_complaint', 
            'nurse_notes',       
        ]
        widgets = {
            'chief_complaint': forms.Textarea(attrs={'rows': 2}),
            'nurse_notes': forms.Textarea(attrs={'rows': 3}),
        }
        
