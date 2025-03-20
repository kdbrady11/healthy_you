from django import forms
from .models import SleepRecord


class SleepRecordForm(forms.ModelForm):
    """
    Form for creating and updating SleepRecord instances.
    Provides input fields for date, duration, and quality with customizable widgets.
    """

    class Meta:
        model = SleepRecord  # Model associated with the form
        fields = ['date', 'duration', 'quality']  # Fields to be displayed in the form
        widgets = {
            # Use HTML5 date input for better user experience
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
