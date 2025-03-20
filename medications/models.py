from django.db import models
from django.contrib.auth.models import User


class Medication(models.Model):
    """
    Represents a medication that a user is taking, along with its schedule and other details.
    """
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The user who is taking this medication."
    )
    name = models.CharField(
        max_length=100,
        help_text="The name of the medication."
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional description or notes about the medication."
    )
    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        help_text="The frequency at which the medication is taken (e.g., daily, weekly)."
    )
    start_date = models.DateField(
        help_text="The date when this medication regimen starts."
    )
    dosing_schedule = models.CharField(
        max_length=100,
        blank=True,
        help_text="General instructions (e.g., 'Take with food')."
    )

    def __str__(self):
        return f"{self.name} ({self.frequency})"


class MedicationDoseTime(models.Model):
    """
    Represents a specific dosing time for a medication, along with an optional recurrence schedule.
    """
    medication = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE,
        related_name='dose_times',
        help_text="Reference to the corresponding medication."
    )
    scheduled_time = models.TimeField(
        help_text="Time of day when the dose should be taken."
    )
    recurring_days = models.CharField(
        max_length=50,
        blank=True,
        help_text="Comma-separated weekdays (e.g., 'Mon,Wed,Fri'). Leave blank for every day."
    )

    def __str__(self):
        return f"{self.medication.name} at {self.scheduled_time}"


class MedicationLog(models.Model):
    """
    Log representing whether a medication was taken or missed for a specific dose time on a given date.
    """
    STATUS_CHOICES = [
        ('taken', 'Taken'),
        ('not_taken', 'Not Taken'),
        ('not_recorded', 'Not Recorded'),
    ]

    medication = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE,
        help_text="Reference to the corresponding medication."
    )
    date = models.DateField(
        help_text="The date for this particular medication log."
    )
    dose_time = models.ForeignKey(
        MedicationDoseTime,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Optional reference to the specific dose time (if applicable)."
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='not_recorded',
        help_text="The status of the medication for this log (e.g., taken or missed)."
    )

    class Meta:
        unique_together = ('medication', 'date', 'dose_time')
        verbose_name = "Medication Log"
        verbose_name_plural = "Medication Logs"

    def __str__(self):
        time_str = f" at {self.dose_time.scheduled_time}" if self.dose_time else ""
        return f"{self.medication.name} on {self.date}{time_str}: {self.status}"
