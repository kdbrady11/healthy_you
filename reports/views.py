import datetime
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, F, ExpressionWrapper, FloatField
from health.models import HealthMetric
from sleep.models import SleepRecord


@login_required
def report_dashboard(request):
    """
    Generates the report dashboard for the last 30 days of user data,
    including aggregated health metrics and sleep data. Provides data
    for visualizations and textual analysis for improvement suggestions.
    """
    # Set the reporting period: last 30 days
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=30)

    # Define an ExpressionWrapper for calculating the Mean Arterial Pressure (MAP)
    map_expr = ExpressionWrapper(
        (F('blood_pressure_systolic') + 2 * F('blood_pressure_diastolic')) / 3.0,
        output_field=FloatField()
    )

    # Query and aggregate HealthMetric data over the past 30 days
    health_qs = HealthMetric.objects.filter(
        user=request.user, date__range=(start_date, today)
    ).order_by('date')
    health_aggregated = health_qs.values('date').annotate(
        avg_weight=Avg('weight'),
        avg_calories=Avg('calories_intake'),
        avg_activity=Avg('physical_activity_minutes'),
        avg_map=Avg(map_expr),  # Aggregate MAP based on the custom ExpressionWrapper
        avg_hr=Avg('heart_rate')
    )

    # Prepare data for health metrics visualizations
    hm_dates = [entry['date'].strftime('%Y-%m-%d') for entry in health_aggregated]
    hm_weight = [entry['avg_weight'] for entry in health_aggregated]
    hm_weight_lbs = [
        round(w * 2.20462, 2) if w is not None else None for w in hm_weight
    ]  # Convert weight from kg to lbs
    hm_calories = [
        round(entry['avg_calories'], 2) if entry['avg_calories'] is not None else None
        for entry in health_aggregated
    ]
    hm_activity = [
        round(entry['avg_activity'], 2) if entry['avg_activity'] is not None else None
        for entry in health_aggregated
    ]
    hm_map = [
        round(entry['avg_map'], 2) if entry['avg_map'] is not None else None
        for entry in health_aggregated
    ]
    hm_hr = [
        round(entry['avg_hr'], 2) if entry['avg_hr'] is not None else None
        for entry in health_aggregated
    ]

    # Query and aggregate SleepRecord data (sum of sleep duration per day)
    sleep_qs = SleepRecord.objects.filter(
        user=request.user, date__range=(start_date, today)
    ).order_by('date')
    sleep_aggregated = sleep_qs.values('date').annotate(
        total_duration=Sum('duration')
    )
    sl_dates = [entry['date'].strftime('%Y-%m-%d') for entry in sleep_aggregated]
    sl_duration = [round(entry['total_duration'], 2) for entry in sleep_aggregated]

    # Helper function to calculate the average of a list while ignoring None values
    def safe_avg(data):
        filtered = [x for x in data if x is not None]
        return round(sum(filtered) / len(filtered), 2) if filtered else 0

    # Calculate overall averages for user feedback
    overall_weight = safe_avg(hm_weight_lbs)
    overall_calories = safe_avg(hm_calories)
    overall_activity = safe_avg(hm_activity)
    overall_map = safe_avg(hm_map)
    overall_hr = safe_avg(hm_hr)
    overall_sleep = safe_avg(sl_duration)

    # Construct textual analysis based on calculated averages
    analysis = (
        f"Over the past 30 days, your average metrics were as follows: "
        f"Weight: {overall_weight} lbs, Calorie Intake: {overall_calories} calories, "
        f"Activity: {overall_activity} minutes, MAP: {overall_map} mmHg, "
        f"Heart Rate: {overall_hr} bpm, and Sleep Duration: {overall_sleep} hours per day. "
    )
    if overall_weight > 180:
        analysis += "Your weight is higher than ideal—consider nutritional adjustments and exercise. "
    if overall_calories > 2500:
        analysis += "Your calorie intake seems high; review portion sizes. "
    if overall_activity < 30:
        analysis += "Your daily physical activity is low; increasing exercise could boost your health. "
    if overall_sleep < 7:
        analysis += "You are not getting enough sleep; aim for at least 7 hours per night. "

    # Pass all data to the template for visualizations and analysis
    context = {
        'hm_dates': json.dumps(hm_dates),
        'hm_weight_lbs': json.dumps(hm_weight_lbs),
        'hm_calories': json.dumps(hm_calories),
        'hm_activity': json.dumps(hm_activity),
        'hm_map': json.dumps(hm_map),
        'hm_hr': json.dumps(hm_hr),
        'sl_dates': json.dumps(sl_dates),
        'sl_duration': json.dumps(sl_duration),
        'analysis': analysis,
    }
    return render(request, 'reports/report_dashboard.html', context)
