from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# View for Homepage
def homepage(request):
    """Homepage view that acts as a central hub for the project."""
    context = {
        "project_title": "Healthy You",
        "project_description": (
            "Healthy You is a powerful platform designed to help users stay on top of their health "
            "by tracking their medications, setting reminders, monitoring health metrics, and achieving "
            "their wellness goals. Simplify your health management with one intuitive interface."
        )
    }
    return render(request, "accounts/homepage.html", context)

# View for user registration
def register(request):
    """
    Handle user registration.
    If the request is POST, process the form data.
    If valid, create the user, log them in, and redirect to the dashboard.
    Otherwise, re-render the form with errors.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Django's built-in user registration form
        if form.is_valid():
            user = form.save()  # Save the new user to the database
            login(request, user)  # Log the user in after successful registration
            messages.success(request, "Registration successful.")  # Success message
            return redirect('dashboard')  # Redirect to the dashboard view
        else:
            messages.error(request, "Registration failed. Please correct the error below.")  # Error message
    else:
        form = UserCreationForm()  # Initialize an empty registration form
    return render(request, 'accounts/register.html', {'form': form})


# View for user login
def user_login(request):
    """
    Handle user login.
    If the request is POST, process the login form.
    If valid, authenticate and log the user in, then redirect to the dashboard.
    Otherwise, return the login form with errors.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Django's built-in login form
        if form.is_valid():
            username = form.cleaned_data.get('username')  # Get username from form
            password = form.cleaned_data.get('password')  # Get password from form
            user = authenticate(username=username, password=password)  # Authenticate user
            if user is not None:
                login(request, user)  # Log the user in
                messages.info(request, f"You are now logged in as {username}.")  # Info message
                return redirect('dashboard')  # Redirect to the dashboard view
            else:
                messages.error(request, "Invalid username or password.")  # Error message for invalid credentials
        else:
            messages.error(request, "Invalid username or password.")  # Error message for invalid form inputs
    else:
        form = AuthenticationForm()  # Initialize an empty login form
    return render(request, 'accounts/login.html', {'form': form})


# View for user logout
def user_logout(request):
    """
    Log the user out and redirect to the login page with a success message.
    """
    logout(request)  # Log out the current user
    messages.info(request, "You have successfully logged out.")  # Info message
    return redirect('login')  # Redirect to the login page


# View for user dashboard (requires authentication)
@login_required
def dashboard(request):
    """
    Render the user's dashboard. Requires the user to be logged in.
    """
    return render(request, 'accounts/dashboard.html')  # Render the dashboard template
