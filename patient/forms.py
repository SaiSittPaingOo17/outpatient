from django import forms
from .models import Patient
from django.contrib.auth.hashers import make_password

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
                    'title',
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
        
    def clean_password(self):
        password = self.cleaned_data['password']
        return make_password(password)