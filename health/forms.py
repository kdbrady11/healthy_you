from django import forms
from .models import HealthMetric


class HealthMetricForm(forms.ModelForm):
    WEIGHT_UNIT_CHOICES = (
        ('kg', 'kg'),
        ('lbs', 'lbs'),
    )
    weight_unit = forms.ChoiceField(choices=WEIGHT_UNIT_CHOICES, initial='kg', label="Weight Unit")

    class Meta:
        model = HealthMetric
        fields = [
            'date',
            'weight',
            'weight_unit',
            'blood_pressure_systolic',
            'blood_pressure_diastolic',
            'heart_rate',
            'calories_intake',
            'physical_activity_minutes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        weight = cleaned_data.get('weight')
        weight_unit = cleaned_data.get('weight_unit')
        if weight is not None and weight_unit == 'lbs':
            # Convert weight from lbs to kg (1 kg ≈ 2.20462 lbs)
            cleaned_data['weight'] = weight / 2.20462
        return cleaned_data
