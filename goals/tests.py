from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Goal
from .forms import GoalForm
import datetime


class GoalModelTest(TestCase):
    """
    Tests for the Goal model.
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Create a test Goal instance
        self.goal = Goal.objects.create(
            user=self.user,
            goal_type='weight',
            target_value=150.5,
            comparison='min',
            description='Lose weight to 150 lbs.',
            due_date=datetime.date.today() + datetime.timedelta(days=30),
        )

    def test_goal_str_method(self):
        """
        Test the __str__ method of the Goal model.
        """
        self.assertEqual(
            str(self.goal),
            "Weight Goal: 150.5 (Minimize)"
        )

    def test_goal_creation(self):
        """
        Test that a Goal instance is correctly created.
        """
        self.assertEqual(Goal.objects.count(), 1)
        self.assertEqual(self.goal.goal_type, 'weight')


class GoalFormTest(TestCase):
    """
    Tests for the GoalForm.
    """

    def setUp(self):
        self.valid_data = {
            'goal_type': 'calories',
            'target_value': 2000,
            'comparison': 'max',
            'description': 'Increase daily calorie intake.',
            'due_date': datetime.date.today() + datetime.timedelta(days=15),
        }
        self.invalid_data = self.valid_data.copy()
        self.invalid_data['target_value'] = ''  # Invalid data

    def test_valid_goal_form(self):
        """
        Test that the GoalForm is valid when provided with correct data.
        """
        form = GoalForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_goal_form(self):
        """
        Test that the GoalForm is invalid when provided with incorrect data.
        """
        form = GoalForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())


class GoalViewsTest(TestCase):
    """
    Tests for the views in the Goals application.
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Log the user in
        self.client = Client()
        self.client.login(username='testuser', password='password123')

        # Create some test Goal instances
        self.goal1 = Goal.objects.create(
            user=self.user,
            goal_type='weight',
            target_value=150.5,
            comparison='min',
            description='Lose weight to 150 lbs.',
            due_date=datetime.date.today() + datetime.timedelta(days=30),
        )
        self.goal2 = Goal.objects.create(
            user=self.user,
            goal_type='activity',
            target_value=60,
            comparison='max',
            description='Increase daily physical activity.',
            due_date=datetime.date.today() + datetime.timedelta(days=15),
        )

    def test_goal_dashboard_view(self):
        """
        Test that the goal_dashboard view loads correctly and displays goals.
        """
        response = self.client.get(reverse('goal_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.goal1.description)
        self.assertContains(response, self.goal2.description)

    def test_goal_create_view_get(self):
        """
        Test that the goal_create view loads correctly (GET request).
        """
        response = self.client.get(reverse('goal_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create')

    def test_goal_create_view_post(self):
        """
        Test that the goal_create view successfully creates a new goal (POST request).
        """
        new_goal_data = {
            'goal_type': 'calories',
            'target_value': 2000,
            'comparison': 'max',
            'description': 'Increase daily calorie intake.',
            'due_date': datetime.date.today() + datetime.timedelta(days=20),
        }
        response = self.client.post(reverse('goal_create'), data=new_goal_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(Goal.objects.count(), 3)  # Ensure a new goal is created

    def test_goal_edit_view_get(self):
        """
        Test that the goal_edit view loads correctly (GET request).
        """
        response = self.client.get(reverse('goal_edit', args=[self.goal1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit')

    def test_goal_edit_view_post(self):
        """
        Test that the goal_edit view successfully updates an existing goal (POST request).
        """
        updated_data = {
            'goal_type': 'weight',
            'target_value': 140,  # Updated target value
            'comparison': 'min',
            'description': self.goal1.description,
            'due_date': self.goal1.due_date,
        }
        response = self.client.post(reverse('goal_edit', args=[self.goal1.id]), data=updated_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.goal1.refresh_from_db()
        self.assertEqual(self.goal1.target_value, 140)


class GoalAccessTest(TestCase):
    """
    Tests to ensure unauthorized access is prevented.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = Client()

    def test_dashboard_requires_login(self):
        """
        Test that the goal_dashboard view redirects unauthenticated users.
        """
        response = self.client.get(reverse('goal_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_create_requires_login(self):
        """
        Test that the goal_create view redirects unauthenticated users.
        """
        response = self.client.get(reverse('goal_create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_edit_requires_login(self):
        """
        Test that the goal_edit view redirects unauthenticated users.
        """
        response = self.client.get(reverse('goal_edit', args=[1]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
