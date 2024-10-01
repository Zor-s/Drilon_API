from django.shortcuts import render, redirect  # Import render function
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

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

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in and redirect to the home page (or another page)
            auth_login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('home')  # Redirect to the home page or a dashboard
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('loginform')

    return render(request, 'portfolio/login.html')