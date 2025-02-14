from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .models import UserProfile
from django.contrib import messages
from django.http import JsonResponse
import uuid
# Create your views here.
def login(request):
    return render(request, 'login.html')

def signup(request):
    form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signupuser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if UserProfile.objects.filter(email=email).exists():
                form.add_error('email', 'This email is already in use.')
                return render(request, 'signup.html', {'form': form})
            
            user = form.save() 
            login(request)  
            user_profile = UserProfile.objects.get(user=user)
            user_profile.token = uuid.uuid4()
            user_profile.save()
            
            # Set the token in a cookie
            response = redirect('/')
            response.set_cookie('auth_token', user_profile.token, max_age=3600*24*30)  # 30 days
            
            return response
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
    
    
def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Debugging: Print received email and password
        print(f"Received email: {username}")
        print(f"Received password: {password}")  # Avoid printing passwords in production!

        user = authenticate(request, username=username, password=password)

        # Debugging: Check if user is found
        if user is not None:
            print(f"User {user.username} authenticated successfully.")

            login(request)
            print("User logged in successfully.")
            return redirect('/')
        else:
            print("Authentication failed. Invalid email or password.")
            messages.error(request, 'Invalid Email or password. Please try again.')
            return redirect('/login')
    else:
        return render(request, 'login.html')
        