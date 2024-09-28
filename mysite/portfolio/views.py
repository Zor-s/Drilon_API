from django.shortcuts import render  # Import render function

def login(request):
    return render(request, 'portfolio/login.html')  # Render the home.html template

def home(request):
    return render(request, 'portfolio/home.html')