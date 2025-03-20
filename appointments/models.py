from django.db import models
from django.contrib.auth.models import User


class Appointment(models.Model):
    """
    Model representing an appointment.
    Each appointment is linked to a user and contains details such as title, date, time, and status.
    """

    # Choices for the appointment status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('attended', 'Attended'),
        ('missed', 'Missed'),
    ]

    # Fields for the Appointment model
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Delete appointments if the user is deleted
        related_name='appointments'  # Reverse relation name for easier querying (e.g., user.appointments.all())
    )
    title = models.CharField(
        max_length=200,
        help_text="Title of the appointment (e.g., Doctor Visit, Meeting)"
    )
    description = models.TextField(
        blank=True,
        help_text="Optional: Provide additional details about the appointment"
    )
    appointment_date = models.DateField(
        help_text="Date of the appointment (YYYY-MM-DD)"
    )
    appointment_time = models.TimeField(
        help_text="Time of the appointment (HH:MM:SS)"
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional: Specify where the appointment will take place"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the appointment"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,  # Automatically set the field to the current timestamp when the object is created
        help_text="Timestamp when the appointment was created"
    )

    def __str__(self):
        """
        String representation of the appointment.
        Example: "Doctor Visit on 2023-10-15 at 14:30"
        """
        return f"{self.title} on {self.appointment_date} at {self.appointment_time}"
