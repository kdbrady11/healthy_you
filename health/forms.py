from django import forms
from .models import HealthMetric


class HealthMetricForm(forms.ModelForm):
    """
    Form for creating or editing a HealthMetric object. Includes additional
    functionality for handling weight unit conversions between kg and lbs.
    """

    # Defining weight unit choices as a tuple
    WEIGHT_UNIT_CHOICES = (
        ('kg', 'kg'),
        ('lbs', 'lbs'),
    )

    # Custom weight unit field to allow user selection between kg and lbs
    weight_unit = forms.ChoiceField(
        choices=WEIGHT_UNIT_CHOICES,
        initial='kg',  # Default value set to kg
        label="Weight Unit"  # Display label for the field
    )

    class Meta:
        """
        Meta configuration for the HealthMetricForm. Links the form to the HealthMetric model
        and specifies fields, widgets, and custom attributes.
        """
        model = HealthMetric
        fields = [
            'date',
            'weight',
            'weight_unit',
            'blood_pressure_systolic',
            'blood_pressure_diastolic',
            'heart_rate',
            'calories_intake',
            'physical_activity_minutes',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # HTML date input for improved UX
        }

    def clean(self):
        """
        Custom clean method to process and validate form data.
        Handles conversion of weight from lbs to kg if the 'weight_unit' is set to 'lbs'.
        """
        cleaned_data = super().clean()  # Access the cleaned data from the form
        weight = cleaned_data.get('weight')  # Retrieve the weight value
        weight_unit = cleaned_data.get('weight_unit')  # Retrieve the selected weight unit

        # Check if weight is provided and needs conversion from lbs to kg
        if weight is not None and weight_unit == 'lbs':
            # Convert weight from lbs to kg (1 kg ≈ 2.20462 lbs)
            cleaned_data['weight'] = weight / 2.20462

        return cleaned_data
