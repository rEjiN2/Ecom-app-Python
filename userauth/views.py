from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignUpForm
from .models import UserProfile
from django.contrib import messages
from django.http import JsonResponse
import uuid


def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
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
            login(request, user)  
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

            login(request, user)
            user_profile = UserProfile.objects.get(user = user)
            user_profile.token = uuid.uuid4()
            user_profile.save()
            print("User logged in successfully.")
            response = redirect('/')
            response.set_cookie('auth_token', user_profile.token, max_age=3600*24*30)  # 30 days
            
            return response
        else:
            print("Authentication failed. Invalid email or password.")
            messages.error(request, 'Invalid Email or password. Please try again.')
            return redirect('/auth/login')
    else:
        return render(request, 'login.html')
        
        
def logout_view(request):
    logout(request)
    response = redirect("/")
    response.delete_cookie('auth_token')
    return response

@login_required
def profile_view(request):
    user = request.user
    profile = user.userprofile 
    context = {
        'user': user,
        'profile': profile,  # Pass the profile to the template
    }
    return render(request, 'profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = user.userprofile
        
        
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.address = request.POST.get('address')
        print("Address: ", user.address)
        user.save()
        
        profile.address = request.POST.get('address')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('/auth/profile')
    
    return redirect('/auth/profile')
       

@login_required
def update_profile_picture(request):
    return "sad"

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user = request.user
        
        # Check if the old password is correct
        if not user.check_password(old_password):
            print("Old Password is incorrect.")
            messages.error(request, 'Old Password is incorrect.')
            return redirect('/auth/profile')
        
        
       # Check if the new password and confirmation match
        if new_password != confirm_password:
            print("New Password and Confirm Password do not match.")
            messages.error(request, 'New Password and Confirm Password do not match.')
            return redirect('/auth/profile')
        
        
        # Set the new password
        user.set_password(new_password)
        user.save()
        
        
        # Update the session to prevent the user from being logged out
        update_session_auth_hash(request, user)
        print('Password changed successfully')
        messages.success(request, 'Password changed successfully!')
        return redirect('/auth/profile')
    
    return render(request, 'profile.html')
        
        