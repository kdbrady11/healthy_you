from django import forms
from .models import Goal


class GoalForm(forms.ModelForm):
    """
    A form for creating or editing Goal instances.
    Utilizes Django's ModelForm for automatic field generation based on the Goal model.
    """

    class Meta:
        model = Goal  # Specify the model this form is associated with
        fields = ['goal_type', 'target_value', 'comparison', 'description', 'due_date']  # Fields to include in the form

        # Custom input widgets for enhanced user experience
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),  # Use HTML5 date input for better date selection
        }
