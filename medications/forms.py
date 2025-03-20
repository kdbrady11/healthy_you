from django import forms
from .models import Medication, MedicationDoseTime


class MedicationForm(forms.ModelForm):
    """
    Form for creating and updating Medication objects.
    """

    class Meta:
        model = Medication  # Model associate with this form
        fields = ['name', 'description', 'frequency', 'start_date', 'dosing_schedule']  # Fields to include in the form
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),  # Use an HTML5 date picker for the start_date field
        }


class MedicationDoseTimeForm(forms.ModelForm):
    """
    Form for handling MedicationDoseTime objects, including times and recurrence.
    """

    class Meta:
        model = MedicationDoseTime  # Model associate with this form
        fields = ['scheduled_time', 'recurring_days']  # Fields to include in the form
        widgets = {
            'scheduled_time': forms.TimeInput(attrs={'type': 'time'}),  # Use an HTML5 time picker for the time field
        }
