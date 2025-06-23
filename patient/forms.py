from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
                    'fname',
                    'lname',
                    'date_of_birth',
                    'gender',
                    'marital_status',
                    'phone',
                    'email',
                    'address',
                    'password',
                 ]
        widgets = {
                    'gender': forms.RadioSelect(), #create radio button
                    'password': forms.PasswordInput(),  # Hides password input
                    'date_of_birth': forms.DateInput(attrs={'type': 'date'}),  # HTML5 date picker
                }