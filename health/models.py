from django.db import models
from django.contrib.auth.models import User


class HealthMetric(models.Model):
    """
    Model representing health metrics recorded by a user on a specific date.
    Includes fields for weight, blood pressure, heart rate, calorie intake,
    and physical activity minutes.
    """

    # Association with the User who records the health metrics
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Automatically deletes metrics if the user is deleted
        help_text="The user associated with these health metrics."
    )

    # Date for the recorded metrics
    date = models.DateField(
        help_text="Select the date for these health metrics."
    )

    # Fields for recording various health metrics
    weight = models.FloatField(
        help_text="Weight of the user in kilograms (kg)."
    )
    blood_pressure_systolic = models.IntegerField(
        null=True,  # Allows null values in the database
        blank=True,  # Optional field in forms and admin interface
        help_text="Systolic blood pressure of the user in mmHg."
    )
    blood_pressure_diastolic = models.IntegerField(
        null=True,
        blank=True,
        help_text="Diastolic blood pressure of the user in mmHg."
    )
    heart_rate = models.IntegerField(
        null=True,
        blank=True,
        help_text="Resting heart rate of the user in beats per minute (BPM)."
    )
    calories_intake = models.IntegerField(
        null=True,
        blank=True,
        help_text="Number of calories consumed by the user on this date."
    )
    physical_activity_minutes = models.IntegerField(
        null=True,
        blank=True,
        help_text="Total minutes of physical activity performed on this date."
    )

    def __str__(self):
        """
        String representation of the HealthMetric object.
        Displays the username and the date of the health metrics.
        """
        return f"{self.user.username} - {self.date}"
