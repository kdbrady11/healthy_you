from django import forms
from .models import SleepRecord

class SleepRecordForm(forms.ModelForm):
    class Meta:
        model = SleepRecord
        fields = ['date', 'duration', 'quality']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
