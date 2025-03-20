import datetime
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm


@login_required
def appointment_dashboard(request):
    """
    View to display the appointment dashboard for the logged-in user.
    Includes both upcoming and past appointments and prepares event data for FullCalendar.
    """
    # Retrieve all appointments specific to the logged-in user
    appointments = Appointment.objects.filter(user=request.user).order_by('appointment_date', 'appointment_time')

    # Prepare events data for FullCalendar
    events = []
    for appt in appointments:
        # Combine date and time into a single datetime object
        dt = datetime.datetime.combine(appt.appointment_date, appt.appointment_time)
        events.append({
            "title": appt.title,
            "start": dt.isoformat(),  # FullCalendar expects dates in ISO format
            "id": appt.id,
        })

    # Get the current date and time
    now = datetime.datetime.now()

    # OLD Appointments: Those that occurred in the past
    old_appointments = appointments.filter(
        appointment_date__lt=now.date()
    ) | appointments.filter(
        appointment_date=now.date(), appointment_time__lt=now.time()
    )
    old_appointments = old_appointments.order_by('appointment_date', 'appointment_time')

    # UPCOMING Appointments: Those that are happening today (in the future) or any future dates
    upcoming_appointments = appointments.filter(
        appointment_date__gt=now.date()
    ) | appointments.filter(
        appointment_date=now.date(), appointment_time__gte=now.time()
    )
    upcoming_appointments = upcoming_appointments.order_by('appointment_date', 'appointment_time')

    # Form for the "Create Appointment" tab
    form = AppointmentForm()

    # Pass all the necessary data into the template context
    context = {
        'appointments': appointments,
        'events': json.dumps(events),  # Convert event data to JSON format for use by FullCalendar
        'old_appointments': old_appointments,
        'upcoming_appointments': upcoming_appointments,
        'form': form,
    }
    return render(request, 'appointments/appointment_dashboard.html', context)


@login_required
def appointment_create(request):
    """
    View to handle the creation of a new appointment.
    Renders the form and validates the user input.
    """
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Create the appointment but don't commit until assigning the user
            appt = form.save(commit=False)
            appt.user = request.user  # Assign the currently logged-in user
            appt.save()
            return redirect('appointment_dashboard')  # Redirect to the dashboard after saving
    else:
        # If GET request, render a new, empty form
        form = AppointmentForm()
    return render(request, 'appointments/appointment_dashboard.html', {'form': form})


@login_required
def appointment_delete(request, appointment_id):
    """
    View to handle appointment deletion.
    Ensures only the owner of the appointment can delete it.
    """
    # Retrieve the appointment or raise a 404 if not found or user doesn't own it
    appt = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    if request.method == 'POST':  # Allow deletion only via POST for safety
        appt.delete()
    # Redirect to the dashboard with the Old Appointments tab active
    return redirect('/appointments/dashboard/?active_tab=old')


@login_required
def appointment_detail(request, pk):
    """
    View to display the details of a specific appointment.
    """
    # Retrieve the specific appointment, or return a 404 if not found
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})
