from django.db import models
from django.contrib.auth.models import User


class SleepRecord(models.Model):
    """
    Model representing a user's sleep record.
    Tracks the date, duration (in hours), and quality (rating from 1 to 5) of sleep.
    """

    # ForeignKey to associate sleep records with a user
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The user who owns this sleep record."
    )

    # Date of the sleep record
    date = models.DateField(
        help_text="The date for which the sleep record is logged."
    )

    # Duration of sleep in hours
    duration = models.FloatField(
        help_text="The duration of sleep in hours."
    )

    # Sleep quality rating from 1 (poor) to 5 (excellent)
    quality = models.IntegerField(
        help_text="Rating for sleep quality (1 - Poor, 5 - Excellent).",
        choices=[(i, i) for i in range(1, 6)],  # Choices for quality rating
        default=3  # Default quality is set to 3 (average)
    )

    def __str__(self):
        """
        String representation of the SleepRecord instance.
        Useful for displaying records in admin pages or debugging.
        """
        return f"{self.user.username} - {self.date} - {self.duration} hrs, quality {self.quality}"

