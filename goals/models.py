from django.db import models
from django.contrib.auth.models import User


class Goal(models.Model):
    """
    A model representing a user's goal, such as weight management, caloric intake,
    physical activity, or sleep. Tracks the goal type, target value, comparison
    direction (minimize or maximize), and associated metadata such as description
    and due date.
    """

    # Available goal types
    GOAL_TYPE_CHOICES = [
        ('weight', 'Weight'),
        ('calories', 'Caloric Intake'),
        ('activity', 'Physical Activity'),
        ('sleep', 'Sleep'),
    ]

    # Comparison choices for determining the goal (e.g., minimize weight, maximize sleep)
    COMPARISON_CHOICES = [
        ('min', 'Minimize'),
        ('max', 'Maximize'),
    ]

    # Model fields
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The user associated with this goal."
    )
    goal_type = models.CharField(
        max_length=20,
        choices=GOAL_TYPE_CHOICES,
        default='weight',
        help_text="The type of goal, such as weight, calories, activity, or sleep."
    )
    target_value = models.FloatField(
        help_text="The target value for the goal (e.g., weight in lbs, calories, activity in minutes, etc.)."
    )
    comparison = models.CharField(
        max_length=10,
        choices=COMPARISON_CHOICES,
        default='min',
        help_text="Specify whether the goal is to minimize or maximize the target value."
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description to provide additional details about the goal."
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="The date by which the goal should be achieved (optional)."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The timestamp when the goal was created."
    )

    def __str__(self):
        """
        Return a human-readable representation of the Goal object.
        Includes goal type, target value, and whether to minimize or maximize.
        """
        return f"{self.get_goal_type_display()} Goal: {self.target_value} ({self.get_comparison_display()})"
