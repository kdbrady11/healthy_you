from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from health.models import HealthMetric
from sleep.models import SleepRecord
import datetime


class ReportDashboardViewTest(TestCase):
    """
    Unit tests for the report_dashboard view in the reports application.
    """

    def setUp(self):
        """
        Set up test data for the view.
        Creates a test user, health metrics, and sleep records
        to test the aggregation and response context.
        """
        # Create a test user and login
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Set test date range: last 30 days
        self.today = datetime.date.today()
        self.start_date = self.today - datetime.timedelta(days=30)

        # Create HealthMetric data for the test user
        HealthMetric.objects.bulk_create([
            HealthMetric(user=self.user, date=self.today - datetime.timedelta(days=i),
                         weight=70 + i,  # Increasing weight (kg)
                         calories_intake=2000 + i * 10,  # Calorie intake increases daily
                         physical_activity_minutes=30 + i,  # Physical activity increases daily
                         blood_pressure_systolic=120 + i,  # Systolic pressure increases
                         blood_pressure_diastolic=80 + i,  # Diastolic pressure increases
                         heart_rate=70 + i)  # Heart rate increases
            for i in range(30)
        ])

        # Create SleepRecord data for the test user
        SleepRecord.objects.bulk_create([
            SleepRecord(user=self.user, date=self.today - datetime.timedelta(days=i),
                        duration=6 + i % 3)  # Sleep duration varies between 6, 7, and 8 hours
            for i in range(30)
        ])

    def test_dashboard_view_status_code(self):
        """
        Test that the report_dashboard view returns a 200 status code.
        """
        response = self.client.get(reverse('report_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_template_used(self):
        """
        Test that the correct template is used in the response.
        """
        response = self.client.get(reverse('report_dashboard'))
        self.assertTemplateUsed(response, 'reports/report_dashboard.html')

    def test_dashboard_view_context_data(self):
        """
        Test that the context contains aggregated data, JSON-serialized arrays for visualizations,
        and a textual analysis string.
        """
        response = self.client.get(reverse('report_dashboard'))
        context = response.context

        # Check that context contains required keys
        expected_keys = [
            'hm_dates', 'hm_weight_lbs', 'hm_calories', 'hm_activity', 'hm_map',
            'hm_hr', 'sl_dates', 'sl_duration', 'analysis'
        ]
        for key in expected_keys:
            self.assertIn(key, context)

        # Assert that the generated analysis contains text
        self.assertIn('Over the past 30 days', context['analysis'])

    def test_aggregated_health_metrics(self):
        """
        Test the aggregation for health metrics, including weight in lbs, calorie intake,
        physical activity, and MAP computations.
        """
        response = self.client.get(reverse('report_dashboard'))
        context = response.context

        # Check that hm_weight_lbs is calculated and matches expected conversion logic
        expected_weights_lbs = [
            round((70 + i) * 2.20462, 2)  # Convert kg to lbs
            for i in range(30)
        ]
        self.assertEqual(json.loads(context['hm_weight_lbs']), expected_weights_lbs)

        # Check calorie data aggregation
        expected_calories = [
            2000 + i * 10
            for i in range(30)
        ]
        self.assertEqual(json.loads(context['hm_calories']), expected_calories)

        # Check MAP and activity using model fields
        expected_activity = [
            30 + i
            for i in range(30)
        ]
        self.assertEqual(json.loads(context['hm_activity']), expected_activity)

    def test_aggregated_sleep_data(self):
        """
        Test the aggregation for sleep data: total duration per day.
        """
        response = self.client.get(reverse('report_dashboard'))
        context = response.context

        # Check sleep duration aggregation
        expected_sleep_durations = [
            round(6 + (i % 3), 2) for i in range(30)
        ]
        self.assertEqual(json.loads(context['sl_duration']), expected_sleep_durations)

        # Check sleep dates
        expected_dates = [
            (self.today - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            for i in range(30)
        ]
        self.assertEqual(json.loads(context['sl_dates']), expected_dates)

    def test_analysis_logic(self):
        """
        Test the logic behind textual analysis generation to verify suggestions for improvement.
        """
        response = self.client.get(reverse('report_dashboard'))
        analysis = response.context['analysis']

        # Check for general text structure
        self.assertIn('Over the past 30 days, your average metrics were as follows', analysis)

        # Check specific advice based on thresholds (e.g., weight, calories, activity, and sleep)
        if any(weight > 180 for weight in json.loads(response.context['hm_weight_lbs'])):
            self.assertIn('Your weight is higher than ideal', analysis)
        if any(calories > 2500 for calories in json.loads(response.context['hm_calories'])):
            self.assertIn('Your calorie intake seems high', analysis)
        if any(activity < 30 for activity in json.loads(response.context['hm_activity'])):
            self.assertIn('Your daily physical activity is low', analysis)
        if any(sleep < 7 for sleep in json.loads(response.context['sl_duration'])):
            self.assertIn('You are not getting enough sleep', analysis)
