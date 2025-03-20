from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    """
    A form for creating and updating Appointment instances.
    Uses Django's ModelForm for automatic model-to-form mapping.
    """

    class Meta:
        model = Appointment  # Specify the model the form is based on
        fields = ['title', 'description', 'appointment_date', 'appointment_time', 'location',
                  'status']  # Explicitly define the fields to include in the form

        # Add custom widgets for better user input experience
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),  # Render a modern HTML5 date picker
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),  # Render a modern HTML5 time picker
        }
