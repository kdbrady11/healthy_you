from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Appointment
from .forms import AppointmentForm
import datetime


class AppointmentModelTest(TestCase):
    """
    Tests for the Appointment model.
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create a test appointment
        self.appointment = Appointment.objects.create(
            user=self.user,
            title="Doctor Visit",
            description="Annual checkup",
            appointment_date=datetime.date.today(),
            appointment_time=datetime.time(9, 30),
            location="Clinic",
            status="pending",
        )

    def test_appointment_str_representation(self):
        """
        Test the string representation of the Appointment model.
        """
        self.assertEqual(
            str(self.appointment),
            f"{self.appointment.title} on {self.appointment.appointment_date} at {self.appointment.appointment_time}",
        )

    def test_default_status_is_pending(self):
        """
        Test the default status of an appointment.
        """
        appointment = Appointment.objects.create(
            user=self.user,
            title="Default Status Test",
            appointment_date=datetime.date.today(),
            appointment_time=datetime.time(9, 0),
        )
        self.assertEqual(appointment.status, "pending")


class AppointmentFormTest(TestCase):
    """
    Tests for the AppointmentForm.
    """

    def test_valid_form(self):
        """
        Test that the form is valid with proper data.
        """
        data = {
            "title": "Meeting",
            "description": "Discuss project details",
            "appointment_date": datetime.date.today(),
            "appointment_time": datetime.time(10, 0),
            "location": "Office",
            "status": "pending",
        }
        form = AppointmentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Test that the form is invalid with missing required fields.
        """
        data = {
            "description": "Missing title and required fields",
        }
        form = AppointmentForm(data=data)
        self.assertFalse(form.is_valid())


class AppointmentViewTest(TestCase):
    """
    Tests for the views in the appointments app.
    """

    def setUp(self):
        # Create a test client
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create test appointments
        self.appointment = Appointment.objects.create(
            user=self.user,
            title="Dentist Appointment",
            description="Clean teeth",
            appointment_date=datetime.date.today(),
            appointment_time=datetime.time(15, 0),
            location="Dental Clinic",
            status="pending",
        )

    def test_dashboard_view_requires_login(self):
        """
        Test that the appointment dashboard redirects if the user is not logged in.
        """
        response = self.client.get(reverse("appointment_dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_dashboard_view_logged_in(self):
        """
        Test that the appointment dashboard loads for a logged-in user.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("appointment_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "appointments/appointment_dashboard.html")

    def test_appointment_create_view(self):
        """
        Test creating an appointment via the appointment_create view.
        """
        self.client.login(username="testuser", password="testpassword")
        data = {
            "title": "New Appointment",
            "description": "Test Description",
            "appointment_date": str(datetime.date.today() + datetime.timedelta(days=1)),
            "appointment_time": "14:00",
            "location": "Test Location",
            "status": "pending",
        }
        response = self.client.post(reverse("appointment_create"), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(Appointment.objects.filter(user=self.user).count(), 2)  # Check if the appointment is added

    def test_appointment_delete_view(self):
        """
        Test deleting an appointment via the appointment_delete view.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("appointment_delete", args=[self.appointment.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Appointment.objects.filter(id=self.appointment.id).exists())  # Ensure it's deleted

    def test_appointment_detail_view(self):
        """
        Test viewing the details of a specific appointment.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("appointment_detail", args=[self.appointment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "appointments/appointment_detail.html")
        self.assertContains(response, self.appointment.title)  # Check that the appointment title is in the response


class AppointmentPermissionsTest(TestCase):
    """
    Tests to ensure that users cannot access or modify appointments they don't own.
    """

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

        # Create an appointment for user1
        self.appointment = Appointment.objects.create(
            user=self.user1,
            title="Private Appointment",
            appointment_date=datetime.date.today(),
            appointment_time=datetime.time(11, 0),
            location="Private Location",
        )
        self.client = Client()

    def test_user_cannot_delete_other_user_appointment(self):
        """
        Ensure a user cannot delete an appointment belonging to another user.
        """
        self.client.login(username="user2", password="password2")
        response = self.client.post(reverse("appointment_delete", args=[self.appointment.id]))
        self.assertEqual(response.status_code, 404)  # Should return 404 because they don't own it

    def test_user_cannot_view_other_user_appointment(self):
        """
        Ensure a user cannot view the details of another user's appointment.
        """
        self.client.login(username="user2", password="password2")
        response = self.client.get(reverse("appointment_detail", args=[self.appointment.id]))
        self.assertEqual(response.status_code, 404)  # Should return 404 because they don't own it
