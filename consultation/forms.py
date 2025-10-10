from django import forms
from .models import Consultation

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = [
            'chief_comp',
            'present_ill',
            'past_med',
            'past_sur',
            'medica_his',
            'og_his',
            'fam_his',
            'soc_his',
            'phy_exam',
            'diag',
            'notes',
        ]