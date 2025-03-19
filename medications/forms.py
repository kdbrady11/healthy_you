from django import forms
from .models import Medication, MedicationDoseTime

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'description', 'frequency', 'start_date', 'dosing_schedule']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MedicationDoseTimeForm(forms.ModelForm):
    class Meta:
        model = MedicationDoseTime
        fields = ['scheduled_time', 'recurring_days']
        widgets = {
            'scheduled_time': forms.TimeInput(attrs={'type': 'time'}),
        }
