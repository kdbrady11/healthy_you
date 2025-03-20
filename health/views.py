import datetime
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, F, ExpressionWrapper, FloatField
from .forms import HealthMetricForm
from .models import HealthMetric


@login_required
def health_dashboard(request):
    """
    View function to display the health dashboard.
    Handles new data entry submission, aggregates metrics over time,
    and provides feedback on the user's health trends.
    """

    # Handle form for new data entry submission
    if request.method == 'POST':
        form = HealthMetricForm(request.POST)
        if form.is_valid():
            metric = form.save(commit=False)
            metric.user = request.user  # Assign current user to the entry
            metric.save()
            return redirect('health_dashboard')
    else:
        form = HealthMetricForm()

    # Define MAP (Mean Arterial Pressure) calculation expression
    map_expr = ExpressionWrapper(
        (F('blood_pressure_systolic') + 2 * F('blood_pressure_diastolic')) / 3.0,
        output_field=FloatField()
    )

    # Aggregate metrics by date for the current user
    aggregated = HealthMetric.objects.filter(user=request.user).values('date').annotate(
        avg_weight=Avg('weight'),
        sum_calories=Sum('calories_intake'),
        sum_activity=Sum('physical_activity_minutes'),
        avg_map=Avg(map_expr),
        avg_hr=Avg('heart_rate')
    ).order_by('date')

    # Extract aggregated data for dashboard graphs
    agg_dates = [entry['date'].strftime('%Y-%m-%d') for entry in aggregated]
    agg_weight = [entry['avg_weight'] for entry in aggregated]
    agg_weight_lbs = [round(w * 2.20462, 2) if w is not None else None for w in agg_weight]
    agg_calories = [entry['sum_calories'] for entry in aggregated]
    agg_activity = [entry['sum_activity'] for entry in aggregated]
    agg_map = [entry['avg_map'] for entry in aggregated]
    agg_hr = [entry['avg_hr'] for entry in aggregated]

    # Calculate overall averages for statistics display
    overall_weight = (sum([w for w in agg_weight_lbs if w is not None]) /
                      len([w for w in agg_weight_lbs if w is not None])) if agg_weight_lbs else 0
    overall_calories = sum(agg_calories) / len(agg_calories) if agg_calories else 0
    overall_activity = sum(agg_activity) / len(agg_activity) if agg_activity else 0
    overall_map = sum(agg_map) / len(agg_map) if agg_map else 0
    overall_hr = sum(agg_hr) / len(agg_hr) if agg_hr else 0

    # Constants for comparison
    NATIONAL_AVG_HR = 70
    NATIONAL_AVG_MAP = 93

    # Generate feedback based on health metrics
    feedback_map = ""
    if agg_map and overall_map:
        latest_map = agg_map[-1]
        feedback_map = (
            "Your MAP is trending above your average—consider stress reduction and a consult if this continues."
            if latest_map > overall_map else "Your MAP is within a healthy range.")

    feedback_weight = ""
    if agg_weight_lbs and overall_weight:
        latest_weight = agg_weight_lbs[-1]
        feedback_weight = ("Your weight is trending upward; review your diet and exercise."
                           if latest_weight > overall_weight else "Your weight appears stable.")

    feedback_hr = ""
    if agg_hr and overall_hr:
        latest_hr = agg_hr[-1]
        feedback_hr = ("Your heart rate is higher than average; consider aerobic exercise and stress management."
                       if latest_hr > overall_hr else "Your heart rate is within normal range.")

    feedback_calories = ""
    if agg_calories and overall_calories:
        latest_calories = agg_calories[-1]
        feedback_calories = ("Your calorie intake is higher than average; adjust portion sizes if needed."
                             if latest_calories > overall_calories else "Your calorie intake is consistent.")

    feedback_activity = ""
    if agg_activity and overall_activity:
        latest_activity = agg_activity[-1]
        feedback_activity = ("Your physical activity is lower than average; try to increase daily movement."
                             if latest_activity < overall_activity else "Your activity level is consistent.")

    # Combine all feedback into a single detailed feedback string
    detailed_feedback = (
        f"<strong>MAP:</strong> {feedback_map}<br>"
        f"<strong>Weight:</strong> {feedback_weight}<br>"
        f"<strong>Heart Rate:</strong> {feedback_hr}<br>"
        f"<strong>Calories:</strong> {feedback_calories}<br>"
        f"<strong>Activity:</strong> {feedback_activity}"
    )

    # Handle filtering for health entries (date range)
    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')
    try:
        if start_date_filter and end_date_filter:
            start_date_obj = datetime.datetime.strptime(start_date_filter, '%Y-%m-%d').date()
            end_date_obj = datetime.datetime.strptime(end_date_filter, '%Y-%m-%d').date()
            entries = HealthMetric.objects.filter(
                user=request.user, date__gte=start_date_obj, date__lte=end_date_obj).order_by('date')
        else:
            entries = HealthMetric.objects.filter(user=request.user).order_by('date')
    except ValueError:
        entries = HealthMetric.objects.filter(user=request.user).order_by('date')

    # Prepare individual metrics for chart rendering
    entries_list = list(entries)
    individual_weight = [
        {"x": entry.date.strftime("%Y-%m-%d"), "y": round(entry.weight * 2.20462, 2)}
        for entry in entries_list if entry.weight is not None
    ]
    individual_hr = [
        {"x": entry.date.strftime("%Y-%m-%d"), "y": entry.heart_rate}
        for entry in entries_list if entry.heart_rate is not None
    ]
    individual_map = [
        {"x": entry.date.strftime("%Y-%m-%d"),
         "y": round((entry.blood_pressure_systolic + 2 * entry.blood_pressure_diastolic) / 3.0, 2)}
        for entry in entries_list if entry.blood_pressure_systolic and entry.blood_pressure_diastolic
    ]

    # Add current date for date range filtering in the frontend
    current_date = datetime.date.today().strftime('%Y-%m-%d')

    # Context data to render
    context = {
        'form': form,
        'agg_dates': json.dumps(agg_dates),
        'agg_weight_lbs': json.dumps(agg_weight_lbs),
        'agg_calories': json.dumps(agg_calories),
        'agg_activity': json.dumps(agg_activity),
        'agg_map': json.dumps(agg_map),
        'agg_hr': json.dumps(agg_hr),
        'overall_weight': overall_weight,
        'overall_calories': overall_calories,
        'overall_activity': overall_activity,
        'overall_map': overall_map,
        'overall_hr': overall_hr,
        'national_avg_hr': NATIONAL_AVG_HR,
        'national_avg_map': NATIONAL_AVG_MAP,
        'feedback': detailed_feedback,
        'entries': entries_list,
        'individual_weight': json.dumps(individual_weight),
        'individual_hr': json.dumps(individual_hr),
        'individual_map': json.dumps(individual_map),
        'current_date': current_date,
    }
    return render(request, 'health/health_dashboard.html', context)


@login_required
def health_edit_entry(request, entry_date):
    """
    View function for editing a health entry for a specific date.
    Handles retrieval, update, and saving of an existing entry.
    """
    try:
        entry_date_obj = datetime.datetime.strptime(entry_date, '%Y-%m-%d').date()
    except ValueError:
        return redirect('health_dashboard')

    entry = get_object_or_404(HealthMetric, user=request.user, date=entry_date_obj)

    if request.method == 'POST':
        form = HealthMetricForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('health_dashboard')
    else:
        form = HealthMetricForm(instance=entry)

    return render(request, 'health/health_edit_entry.html', {'form': form, 'entry_date': entry_date})
