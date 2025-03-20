import datetime
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from .forms import SleepRecordForm
from .models import SleepRecord


@login_required
def sleep_dashboard(request):
    """
    View for the sleep dashboard.
    Handles sleep data entry, calculations for aggregated data, and provides feedback to the user.
    """

    # Handle POST requests to process new sleep data
    if request.method == 'POST':
        form = SleepRecordForm(request.POST)
        if form.is_valid():
            # Save the submitted sleep record
            record = form.save(commit=False)
            record.user = request.user  # Assign the current logged-in user
            record.save()
            return redirect('sleep_dashboard')  # Redirect to the dashboard after saving
    else:
        # Initialize an empty form for GET requests
        form = SleepRecordForm()

    # ** Aggregate sleep data by date for the logged-in user **
    # - Calculate total sleep duration per day (sum)
    # - Calculate average sleep quality per day (average)
    aggregated = SleepRecord.objects.filter(user=request.user).values('date').annotate(
        sum_duration=Sum('duration'),  # Total sleep durations per day
        avg_quality=Avg('quality')  # Average quality per day
    ).order_by('date')  # Order by date (ascending)

    # ** Format aggregated data ready for visualization **
    agg_dates = [entry['date'].strftime('%b %Y') for entry in aggregated]  # Format dates as "Mon YYYY"
    agg_duration = [round(entry['sum_duration'], 2) for entry in aggregated]  # Total hours
    agg_quality = [round(entry['avg_quality'], 2) for entry in aggregated]  # Average quality

    # Calculate overall averages for duration and quality
    overall_duration = sum(agg_duration) / len(agg_duration) if agg_duration else 0
    overall_quality = sum(agg_quality) / len(agg_quality) if agg_quality else 0

    # Build scatter data for individual sleep records, useful for detailed visualizations
    records = SleepRecord.objects.filter(user=request.user).order_by('date')  # Get individual records
    individual_duration = [
        {"x": r.date.strftime("%b %Y"), "y": r.duration} for r in records
    ]
    individual_quality = [
        {"x": r.date.strftime("%b %Y"), "y": r.quality} for r in records
    ]

    # ** Build dynamic feedback based on user statistics **
    feedback = (
        "Your sleep dashboard shows an average total sleep of {:.2f} hours and an average quality of {:.1f} out of 5. "
        .format(overall_duration, overall_quality)
    )

    # Add additional feedback based on sleep stats
    if overall_duration < 7:
        feedback += (
            "You might be getting insufficient sleep; consider establishing a consistent sleep schedule and reducing screen time before bed. "
        )
    else:
        feedback += "Your sleep duration is in a healthy range. "

    if overall_quality < 3:
        feedback += (
            "Your sleep quality is low; consider optimizing your sleep environment (e.g., keeping your room cool and dark) and reducing caffeine in the evening."
        )
    else:
        feedback += "Your sleep quality appears satisfactory."

    # ** Prepare context for the template **
    context = {
        'form': form,  # Form for sleep data entry
        'agg_dates': json.dumps(agg_dates),  # Aggregated dates for visualization
        'agg_duration': json.dumps(agg_duration),  # Aggregated durations
        'agg_quality': json.dumps(agg_quality),  # Aggregated quality ratings
        'overall_duration': overall_duration,  # Overall average sleep duration
        'overall_quality': overall_quality,  # Overall average sleep quality
        'individual_duration': json.dumps(individual_duration),  # Scatter data: individual duration
        'individual_quality': json.dumps(individual_quality),  # Scatter data: individual quality
        'feedback': feedback,  # Personalized feedback for the user
        'records': records,  # Full list of user's records (potentially for editing later)
    }

    # Render the sleep dashboard template with the provided context
    return render(request, 'sleep/sleep_dashboard.html', context)
