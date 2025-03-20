from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AccountsAppTests(TestCase):
    def setUp(self):
        """
        Set up a test user to be used across tests.
        """
        self.test_user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )

    def test_register_view_get(self):
        """
        Test that the register view loads properly with a valid GET request.
        """
        response = self.client.get(reverse('register'))  # Get the register page
        self.assertEqual(response.status_code, 200)  # Check if the page loads successfully
        self.assertTemplateUsed(response, 'accounts/register.html')  # Ensure the right template is used

    def test_register_view_post_valid(self):
        """
        Test that the register view allows successful user registration.
        """
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'strong_password_1',
            'password2': 'strong_password_1',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect upon successful registration
        self.assertRedirects(response, reverse('dashboard'))  # Redirect to the dashboard
        self.assertTrue(User.objects.filter(username='newuser').exists())  # Confirm new user is created

    def test_register_view_post_invalid(self):
        """
        Test that errors are displayed when registration fails.
        """
        response = self.client.post(reverse('register'), {
            'username': '',  # Invalid username
            'password1': 'short',
            'password2': 'differentpassword',
        })
        self.assertEqual(response.status_code, 200)  # Form re-renders with errors on invalid data
        self.assertContains(response, "This field is required.")  # Specific error message for the username

    def test_login_view_get(self):
        """
        Test that the login view loads properly with a valid GET request.
        """
        response = self.client.get(reverse('login'))  # Get the login page
        self.assertEqual(response.status_code, 200)  # Check if the page loads successfully
        self.assertTemplateUsed(response, 'accounts/login.html')  # Ensure the right template is used

    def test_login_view_post_valid(self):
        """
        Test that a valid user can log in.
        """
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect upon successful login
        self.assertRedirects(response, reverse('dashboard'))  # Redirect to the dashboard

    def test_login_view_post_invalid(self):
        """
        Test that errors are displayed when login fails.
        """
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)  # Form re-renders with errors on invalid data
        self.assertContains(response, "Invalid username or password.")  # Specific error message for login failure

    def test_logout_view(self):
        """
        Test that a logged-in user can log out successfully.
        """
        # Log the test user in
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))  # Logout
        self.assertEqual(response.status_code, 302)  # Logout should redirect
        self.assertRedirects(response, reverse('login'))  # Redirect to login page
        response = self.client.get(reverse('dashboard'))  # Attempt to access dashboard after logout
        self.assertEqual(response.status_code, 302)  # Should redirect since user is not logged in

    def test_dashboard_view_logged_in(self):
        """
        Test that the dashboard view is accessible to a logged-in user.
        """
        self.client.login(username='testuser', password='password123')  # Log the test user in
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)  # Dashboard should load successfully
        self.assertTemplateUsed(response, 'accounts/dashboard.html')  # Ensure the right template is used

    def test_dashboard_view_logged_out(self):
        """
        Test that the dashboard redirects to the login page for logged-out users.
        """
        response = self.client.get(reverse('dashboard'))  # Attempt to access dashboard without login
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")  # Login redirection with next
