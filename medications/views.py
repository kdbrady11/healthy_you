import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Medication, MedicationDoseTime, MedicationLog
from .forms import MedicationForm, MedicationDoseTimeForm


@login_required
def medications_dashboard(request):
    """
    Displays the dashboard for the logged-in user's medications,
    showing today's logs and adherence statistics.
    """
    today = datetime.date.today()

    # Get all medications for the current user
    medications = Medication.objects.filter(user=request.user)

    # Build today's logs by iterating over each medication's dose times
    today_logs = []
    for med in medications:
        for dose in med.dose_times.all():
            # Check if today matches the recurring days (if any)
            if dose.recurring_days:
                days = [d.strip() for d in dose.recurring_days.split(',')]
                if today.strftime("%a") not in days:
                    continue

            # Create or retrieve today's log for this dose
            log, created = MedicationLog.objects.get_or_create(
                medication=med,
                date=today,
                dose_time=dose,
                defaults={'status': 'not_recorded'}
            )
            today_logs.append(log)

    # Compute adherence statistics for today
    today_taken = sum(1 for log in today_logs if log.status == 'taken')
    today_not_taken = sum(1 for log in today_logs if log.status == 'not_taken')
    today_not_recorded = sum(1 for log in today_logs if log.status == 'not_recorded')

    # Compute overall adherence across all logs
    all_logs = MedicationLog.objects.filter(medication__user=request.user)
    overall_taken = all_logs.filter(status='taken').count()
    overall_not_taken = all_logs.filter(status='not_taken').count()
    overall_not_recorded = all_logs.filter(status='not_recorded').count()

    # Context for the dashboard template
    context = {
        'medications': medications,
        'today': today,
        'today_logs': today_logs,
        'today_taken': today_taken,
        'today_not_taken': today_not_taken,
        'today_not_recorded': today_not_recorded,
        'overall_taken': overall_taken,
        'overall_not_taken': overall_not_taken,
        'overall_not_recorded': overall_not_recorded,
    }

    return render(request, 'medications/medications_dashboard.html', context)


@login_required
def medication_create(request):
    """
    Allows the user to create a new medication and its associated dose times.
    """
    DoseTimeFormSet = inlineformset_factory(
        Medication,
        MedicationDoseTime,
        form=MedicationDoseTimeForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        med_form = MedicationForm(request.POST)
        if med_form.is_valid():
            # Save the medication instance
            medication = med_form.save(commit=False)
            medication.user = request.user
            medication.save()

            # Bind the inline formset and validate it
            formset = DoseTimeFormSet(request.POST, instance=medication)
            if formset.is_valid():
                formset.save()
                return redirect('medications_dashboard')
    else:
        # Initialize empty forms
        med_form = MedicationForm()
        formset = DoseTimeFormSet(instance=Medication())

    return render(request, 'medications/medication_form.html', {
        'form': med_form,
        'formset': formset,
        'action': 'Create'
    })


@login_required
def medication_edit(request, med_id):
    """
    Allows the user to edit an existing medication and its associated dose times.
    """
    medication = get_object_or_404(Medication, id=med_id, user=request.user)
    DoseTimeFormSet = inlineformset_factory(
        Medication,
        MedicationDoseTime,
        form=MedicationDoseTimeForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        med_form = MedicationForm(request.POST, instance=medication)
        formset = DoseTimeFormSet(request.POST, instance=medication)
        if med_form.is_valid() and formset.is_valid():
            med_form.save()
            formset.save()
            return redirect('medications_dashboard')
    else:
        # Populate forms with existing data
        med_form = MedicationForm(instance=medication)
        formset = DoseTimeFormSet(instance=medication)

    return render(request, 'medications/medication_form.html', {
        'form': med_form,
        'formset': formset,
        'action': 'Edit'
    })


@login_required
def add_dose_time(request, med_id):
    """
    Allows the user to add a new dose time to an existing medication.
    """
    medication = get_object_or_404(Medication, id=med_id, user=request.user)

    if request.method == 'POST':
        dose_form = MedicationDoseTimeForm(request.POST)
        if dose_form.is_valid():
            # Save the dose time
            dose_time = dose_form.save(commit=False)
            dose_time.medication = medication
            dose_time.save()
            return redirect('medication_edit', med_id=medication.id)
    else:
        # Display an empty form for adding a dose time
        dose_form = MedicationDoseTimeForm()

    return render(request, 'medications/dose_time_form.html', {
        'form': dose_form,
        'medication': medication
    })


@login_required
def update_medication_log(request, log_id):
    """
    Updates the status of a medication log record (e.g., 'taken', 'not_taken').
    """
    log = get_object_or_404(MedicationLog, id=log_id, medication__user=request.user)

    if request.method == 'POST':
        # Get the new status from the POST request
        new_status = request.POST.get('status')
        if new_status in dict(MedicationLog.STATUS_CHOICES).keys():
            log.status = new_status
            log.save()

    # Redirect back to the dashboard with optional query parameters
    dashboard_url = reverse('medications_dashboard')
    return redirect(f"{dashboard_url}?active_tab=today")
