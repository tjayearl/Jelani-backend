from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def register(request):
    """
    Handles user registration using a custom form to include email and phone number.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # You could add a success message here using django.contrib.messages
            # and then log the user in automatically with: login(request, user)
            return redirect('login')  # 'login' is the name of the URL from django.contrib.auth.urls
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
