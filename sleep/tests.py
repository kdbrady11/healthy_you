from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import SleepRecord
import datetime


class SleepRecordModelTestCase(TestCase):
    """
    Tests for the SleepRecord model.
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a SleepRecord instance
        self.record = SleepRecord.objects.create(
            user=self.user,
            date=datetime.date(2023, 10, 1),
            duration=7.5,
            quality=4
        )

    def test_sleep_record_creation(self):
        # Ensure the SleepRecord instance is created correctly
        self.assertEqual(self.record.user, self.user)
        self.assertEqual(self.record.date, datetime.date(2023, 10, 1))
        self.assertEqual(self.record.duration, 7.5)
        self.assertEqual(self.record.quality, 4)

    def test_sleep_record_str_representation(self):
        # Test the string representation of a SleepRecord instance
        self.assertEqual(
            str(self.record),
            f"{self.user.username} - {self.record.date} - {self.record.duration} hrs, quality {self.record.quality}"
        )


class SleepDashboardViewTestCase(TestCase):
    """
    Tests for the sleep_dashboard view.
    """

    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Create some SleepRecord instances for the user
        SleepRecord.objects.create(
            user=self.user,
            date=datetime.date(2023, 10, 1),
            duration=7.5,
            quality=4
        )
        SleepRecord.objects.create(
            user=self.user,
            date=datetime.date(2023, 10, 2),
            duration=6.0,
            quality=3
        )

    def test_dashboard_view_status_code(self):
        # Test if the dashboard is accessible for logged-in users
        response = self.client.get(reverse('sleep_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_template(self):
        # Test if the correct template is used for the dashboard
        response = self.client.get(reverse('sleep_dashboard'))
        self.assertTemplateUsed(response, 'sleep/sleep_dashboard.html')

    def test_dashboard_aggregated_data(self):
        # Test if aggregated data is calculated correctly
        response = self.client.get(reverse('sleep_dashboard'))
        self.assertEqual(response.context['overall_duration'], 6.75)  # Average duration
        self.assertEqual(response.context['overall_quality'], 3.5)  # Average quality

    def test_dashboard_individual_records(self):
        # Test if individual records are passed properly in the context
        response = self.client.get(reverse('sleep_dashboard'))
        self.assertEqual(len(response.context['records']), 2)  # Should have 2 records
        self.assertEqual(response.context['records'][0].duration, 7.5)
        self.assertEqual(response.context['records'][1].duration, 6.0)

    def test_dashboard_post_request(self):
        # Test POST request to create a new SleepRecord
        new_record_data = {
            "date": "2023-10-03",
            "duration": 8.0,
            "quality": 5
        }
        response = self.client.post(reverse('sleep_dashboard'), new_record_data)
        self.assertEqual(response.status_code, 302)  # Expect redirect after success

        # Ensure a new record is created
        new_record = SleepRecord.objects.get(date="2023-10-03")
        self.assertEqual(new_record.duration, 8.0)
        self.assertEqual(new_record.quality, 5)


class SleepDashboardAccessTestCase(TestCase):
    """
    Additional tests for access control.
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_dashboard_without_login(self):
        # Ensure the dashboard cannot be accessed without logging in
        response = self.client.get(reverse('sleep_dashboard'))
        self.assertNotEqual(response.status_code, 200)  # Should redirect to login
        self.assertEqual(response.status_code, 302)  # Redirect to login page


class SleepRecordFormTestCase(TestCase):
    """
    Tests for the SleepRecordForm.
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_form_valid_data(self):
        # Test form submission with valid data
        form_data = {
            "date": "2023-10-05",
            "duration": 7.0,
            "quality": 4
        }
        form = SleepRecordForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        # Test form submission with invalid data
        form_data = {
            "date": "invalid-date",
            "duration": "not-a-number",
            "quality": "invalid-quality"
        }
        form = SleepRecordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)
        self.assertIn("duration", form.errors)
        self.assertIn("quality", form.errors)
