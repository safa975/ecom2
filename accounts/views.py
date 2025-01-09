from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import Address
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404



# Get the User model
User = get_user_model()

def register(request):
    if request.method == 'POST':
        print(f"POST data received: {request.POST}")
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '').strip()  
        password2 = request.POST.get('password2', '').strip()  

        # Check for missing fields
        if not email or not username or not password1 or not password2:
            messages.error(request, "All fields are required.")
            print(f"Validation failed: email='{email}', username='{username}', password1='{password1}', password2='{password2}'")
            return redirect('register')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email.")
            return redirect('register')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('register')

        # Generate OTP
        otp = random.randint(100000, 999999)

        # Save OTP and user data in session
        request.session['registration_data'] = {
            'email': email,
            'username': username,
            'password1': password1,  # Store password1 for later use
            'otp': otp
        }

        # Send OTP to the user's email
        try:
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, f"Failed to send OTP. Please try again later. Error: {e}")
            return redirect('register')

        messages.success(request, "OTP sent to your email. Please verify.")
        return redirect('verify_otp')

    return render(request, 'core/accounts/register.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        registration_data = request.session.get('registration_data')

        if not registration_data:
            messages.error(request, "Session expired. Please register again.")
            return redirect('register')

        # Ensure OTP is entered
        if not entered_otp:
            messages.error(request, "OTP is required.")
            return redirect('verify_otp')

        # Check OTP
        if str(entered_otp) == str(registration_data['otp']):
            # Save user to the database
            User.objects.create_user(
                username=registration_data['username'],
                email=registration_data['email'],
                password=registration_data['password1']  # Use password1 for user creation
            )
            messages.success(request, "Registration successful!")
            del request.session['registration_data']  # Clear session data
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'core/accounts/verify_otp.html')

# Other views (login, logout, profile, etc.) remain unchanged




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:index')  # Ensure 'index' is defined in core/urls.py
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'core/accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('core:index')

@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'core/accounts/profile.html', {'addresses': addresses})

@login_required
def add_address(request):
    if request.method == 'POST':
        # Validate the required fields
        required_fields = ['name', 'street', 'city', 'state', 'zipcode', 'phone']
        for field in required_fields:
            if not request.POST.get(field):
                messages.error(request, f"{field.capitalize()} is required.")
                return redirect('profile')

        Address.objects.create(
            user=request.user,
            name=request.POST['name'],
            street=request.POST['street'],
            city=request.POST['city'],
            state=request.POST['state'],
            zipcode=request.POST['zipcode'],
            phone=request.POST['phone']
        )
        messages.success(request, "Address added successfully.")
    return redirect('profile')
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk)
    address.delete()
    return redirect('profile')
