from django import forms
from .models import HealthMetric

class HealthMetricForm(forms.ModelForm):
    class Meta:
        model = HealthMetric
        fields = [
            'date',
            'weight',
            'blood_pressure_systolic',
            'blood_pressure_diastolic',
            'heart_rate',
            'calories_intake',
            'physical_activity_minutes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
