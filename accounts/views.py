from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def signup_view(request):
    """
    Handles user registration. 
    1. If GET: Display the blank form.
    2. If POST: Validate data, create user, log them in, and redirect.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            user = form.save()
            
            # Log the user in immediately (Industry Standard UX)
            login(request, user)
            
            # Redirect to homepage or dashboard
            return redirect('index') 
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})
