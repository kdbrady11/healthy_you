import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from health.models import HealthMetric  # For weight, calories, activity
from sleep.models import SleepRecord  # For sleep duration
from .models import Goal
from .forms import GoalForm


@login_required
def goal_dashboard(request):
    """
    Displays a dashboard with all goals created by the logged-in user.
    Fetches current progress and provides feedback for each goal.
    """
    goals = Goal.objects.filter(user=request.user).order_by('-due_date')  # Fetch user goals sorted by due date
    goal_data = []

    # Define a 7-day window to compute performance for relevant goals
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)

    for goal in goals:
        current_value = None

        # Handle different types of goals
        if goal.goal_type == 'weight':
            # For weight, fetch the latest HealthMetric record
            latest_record = HealthMetric.objects.filter(user=request.user).order_by('-date').first()
            if latest_record and latest_record.weight is not None:
                current_value = round(latest_record.weight * 2.20462, 2)  # Convert to lbs
        elif goal.goal_type in ['calories', 'activity']:
            # For calories and activity, compute a 7-day average
            metric_records = HealthMetric.objects.filter(user=request.user, date__range=[seven_days_ago, today])
            if goal.goal_type == 'calories':
                current_value = metric_records.aggregate(avg=Avg('calories_intake'))['avg']
            elif goal.goal_type == 'activity':
                current_value = metric_records.aggregate(avg=Avg('physical_activity_minutes'))['avg']

            if current_value is not None:
                current_value = round(current_value, 2)
        elif goal.goal_type == 'sleep':
            # For sleep, compute a 7-day average
            sleep_records = SleepRecord.objects.filter(user=request.user, date__range=[seven_days_ago, today])
            current_value = sleep_records.aggregate(avg=Avg('duration'))['avg']
            if current_value is not None:
                current_value = round(current_value, 2)

        # Calculate progress percentage
        progress = None
        if current_value is not None and goal.target_value:
            if goal.comparison == 'max':
                progress = min(100, (current_value / goal.target_value) * 100)
            else:
                progress = min(100, (goal.target_value / current_value) * 100)
            progress = round(progress, 2)

        # Provide tailored feedback for each goal
        feedback = ""
        if current_value is not None:
            if goal.goal_type == 'weight':
                feedback = (
                    "Your current weight meets your goal." if
                    ((goal.comparison == 'min' and current_value <= goal.target_value) or
                     (goal.comparison == 'max' and current_value >= goal.target_value))
                    else "Consider adjusting your diet or exercise to achieve your weight goal."
                )
            elif goal.goal_type == 'calories':
                feedback = (
                    "Your calorie intake meets your goal." if current_value <= goal.target_value
                    else "Consider reducing your calorie intake to meet your target."
                )
            elif goal.goal_type == 'activity':
                feedback = (
                    "Your activity level meets your goal." if current_value >= goal.target_value
                    else "Increase your activity to reach your physical activity goal."
                )
            elif goal.goal_type == 'sleep':
                feedback = (
                    "Your sleep duration meets your goal." if current_value >= goal.target_value
                    else "Try to improve your sleep habits to meet your target."
                )

        # Collect goal context data
        goal_data.append({
            'goal': goal,
            'current_value': current_value,
            'progress': progress,
            'feedback': feedback,
        })

    context = {'goal_data': goal_data}
    return render(request, 'goals/goal_dashboard.html', context)


@login_required
def goal_create(request):
    """
    Handles the creation of a new goal for the logged-in user.
    """
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user  # Associate the goal with the logged-in user
            goal.save()
            return redirect('goal_dashboard')  # Redirect to the dashboard after saving
    else:
        form = GoalForm()

    # Render form template with context
    return render(request, 'goals/goal_form.html', {'form': form, 'action': 'Create'})


@login_required
def goal_edit(request, goal_id):
    """
    Handles editing an existing goal for the logged-in user.
    """
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)  # Ensure the goal belongs to the user
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goal_dashboard')  # Redirect to the dashboard after saving changes
    else:
        form = GoalForm(instance=goal)

    # Render form template with context
    return render(request, 'goals/goal_form.html', {'form': form, 'action': 'Edit'})
