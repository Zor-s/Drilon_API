from django.shortcuts import render, redirect  # Import render function
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .models import LoginAttempt

def login(request):
    return render(request, 'portfolio/login.html')  # Render the home.html template

def home(request):
    return render(request, 'portfolio/home.html')

def signup(request):
    return render(request, 'portfolio/signup.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # Create a new user
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('home')  # Redirect to the login page after successful signup
        except Exception as e:
            messages.error(request, "Error creating account. Please try again.")
            return redirect('signup')

    return render(request, 'portfolio/signup.html')  # Render the signup page if GET request



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
            login_attempt, created = LoginAttempt.objects.get_or_create(user=user)
            
            if login_attempt.is_locked:
                messages.error(request, "Account is locked due to multiple failed login attempts.")
                return redirect('loginform')

        except User.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect('loginform')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Reset failed attempts on successful login
            login_attempt.failed_attempts = 0
            login_attempt.is_locked = False
            login_attempt.save()

            # Log the user in
            auth_login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('home')
        else:
            # Increase failed attempts and lock if necessary
            login_attempt.failed_attempts += 1
            if login_attempt.failed_attempts >= 3:
                login_attempt.is_locked = True
            login_attempt.save()
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('loginform')

    return render(request, 'portfolio/login.html')
