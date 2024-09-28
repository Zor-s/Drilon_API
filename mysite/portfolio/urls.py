from django.urls import path
from .views import login, home  # Import the home view

urlpatterns = [
    path('', login, name='login'),  # Map the root URL to the login view
    path('home/', home, name='home'),  # Map the /home URL to the home view
]
