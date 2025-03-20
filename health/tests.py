from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import HealthMetric
from .forms import HealthMetricForm


class HealthMetricModelTest(TestCase):
    """
    Test cases for the HealthMetric model.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.metric = HealthMetric.objects.create(
            user=self.user,
            date=now().date(),
            weight=70.5,
            blood_pressure_systolic=120,
            blood_pressure_diastolic=80,
            heart_rate=72,
            calories_intake=2500,
            physical_activity_minutes=30,
        )

    def test_model_string_representation(self):
        """
        Test the string representation of the HealthMetric model.
        """
        self.assertEqual(str(self.metric), f"{self.user.username} - {self.metric.date}")

    def test_model_fields(self):
        """
        Test the values of fields for a HealthMetric instance.
        """
        self.assertEqual(self.metric.weight, 70.5)
        self.assertEqual(self.metric.blood_pressure_systolic, 120)
        self.assertEqual(self.metric.blood_pressure_diastolic, 80)
        self.assertEqual(self.metric.heart_rate, 72)
        self.assertEqual(self.metric.calories_intake, 2500)
        self.assertEqual(self.metric.physical_activity_minutes, 30)


class HealthMetricFormTest(TestCase):
    """
    Test cases for the HealthMetricForm.
    """

    def test_form_valid_data(self):
        """
        Test the form with valid data.
        """
        form = HealthMetricForm(data={
            'date': now().date(),
            'weight': 70.5,
            'blood_pressure_systolic': 120,
            'blood_pressure_diastolic': 80,
            'heart_rate': 72,
            'calories_intake': 2500,
            'physical_activity_minutes': 30,
            'weight_unit': 'kg'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """
        Test the form with invalid data.
        """
        form = HealthMetricForm(data={
            'date': 'not_a_date',
            'weight': 'invalid_weight'
        })
        self.assertFalse(form.is_valid())

    def test_form_weight_conversion(self):
        """
        Test if the weight conversion from lbs to kg works in the clean method.
        """
        form = HealthMetricForm(data={
            'date': now().date(),
            'weight': 154,  # weight in lbs
            'blood_pressure_systolic': 120,
            'blood_pressure_diastolic': 80,
            'heart_rate': 72,
            'calories_intake': 2500,
            'physical_activity_minutes': 30,
            'weight_unit': 'lbs'
        })
        if form.is_valid():
            cleaned_data = form.clean()
            self.assertAlmostEqual(cleaned_data['weight'], 154 / 2.20462, places=2)


class HealthDashboardViewTest(TestCase):
    """
    Test cases for the health_dashboard view.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.metric = HealthMetric.objects.create(
            user=self.user,
            date=now().date(),
            weight=70.5,
            blood_pressure_systolic=120,
            blood_pressure_diastolic=80,
            heart_rate=72,
            calories_intake=2500,
            physical_activity_minutes=30,
        )

    def test_dashboard_url_exists(self):
        """
        Test if the dashboard URL is available for logged-in users.
        """
        response = self.client.get(reverse('health_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template_used(self):
        """
        Test if the correct template is used in the dashboard view.
        """
        response = self.client.get(reverse('health_dashboard'))
        self.assertTemplateUsed(response, 'health/health_dashboard.html')

    def test_dashboard_context(self):
        """
        Test if the context contains the necessary keys.
        """
        response = self.client.get(reverse('health_dashboard'))
        self.assertIn('form', response.context)
        self.assertIn('entries', response.context)
        self.assertIn('feedback', response.context)
        self.assertIn('overall_weight', response.context)

    def test_dashboard_redirect_unauthenticated(self):
        """
        Test if unauthenticated users are redirected to the login page.
        """
        self.client.logout()
        response = self.client.get(reverse('health_dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('health_dashboard')}")


class HealthEditEntryViewTest(TestCase):
    """
    Test cases for the health_edit_entry view.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.metric = HealthMetric.objects.create(
            user=self.user,
            date=now().date(),
            weight=70.5,
            blood_pressure_systolic=120,
            blood_pressure_diastolic=80,
            heart_rate=72,
            calories_intake=2500,
            physical_activity_minutes=30,
        )

    def test_edit_entry_url_exists(self):
        """
        Test if the edit entry URL is available for logged-in users.
        """
        response = self.client.get(reverse('health_edit_entry', kwargs={'entry_date': self.metric.date}))
        self.assertEqual(response.status_code, 200)

    def test_edit_entry_template_used(self):
        """
        Test if the correct template is used in the edit entry view.
        """
        response = self.client.get(reverse('health_edit_entry', kwargs={'entry_date': self.metric.date}))
        self.assertTemplateUsed(response, 'health/health_edit_entry.html')

    def test_edit_entry_form_initial_values(self):
        """
        Test if the form is pre-filled with existing data.
        """
        response = self.client.get(reverse('health_edit_entry', kwargs={'entry_date': self.metric.date}))
        self.assertEqual(response.context['form'].initial['weight'], self.metric.weight)

    def test_edit_entry_post_valid_data(self):
        """
        Test if valid POST data updates the entry.
        """
        response = self.client.post(
            reverse('health_edit_entry', kwargs={'entry_date': self.metric.date}),
            data={
                'date': self.metric.date,
                'weight': 75.0,
                'blood_pressure_systolic': 130,
                'blood_pressure_diastolic': 85,
                'heart_rate': 80,
                'calories_intake': 2600,
                'physical_activity_minutes': 40,
                'weight_unit': 'kg'
            }
        )
        self.metric.refresh_from_db()
        self.assertEqual(self.metric.weight, 75.0)
        self.assertEqual(self.metric.blood_pressure_systolic, 130)
        self.assertRedirects(response, reverse('health_dashboard'))

    def test_edit_entry_redirect_unauthenticated(self):
        """
        Test if unauthenticated users are redirected to the login page.
        """
        self.client.logout()
        response = self.client.get(reverse('health_edit_entry', kwargs={'entry_date': self.metric.date}))
        self.assertRedirects(response,
                             f"{reverse('login')}?next={reverse('health_edit_entry', kwargs={'entry_date': self.metric.date})}")
