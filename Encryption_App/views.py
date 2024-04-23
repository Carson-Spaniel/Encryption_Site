from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .AES import AES_encrypt
from .models import UserProfile

def encrypt_file(request):
    if request.method == 'POST' and request.FILES['uploaded_file']:
        uploaded_file = request.FILES['uploaded_file']

        # Check if a key file or a password was provided
        if 'key_file' in request.FILES:
            key_file = request.FILES['key_file']
            aes_key = key_file.read()
        elif 'password' in request.POST:
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password == confirm_password:
                aes_key = AES_encrypt.hash_string(password)
            else:
                return {'error': 'Passwords do not match.'}
        else:
            # Handle case where neither key file nor password was provided
            return {'error': 'Please provide a key file or a password.'}

        response = AES_encrypt.encrypt(uploaded_file, aes_key)

        return response

    return render(request, 'encrypt.html')

def decrypt_file(request):
    if request.method == 'POST' and request.FILES['uploaded_file']:
        uploaded_file = request.FILES['uploaded_file']

        # Check if a key file or a password was provided
        if 'key_file' in request.FILES:
            key_file = request.FILES['key_file']
            aes_key = key_file.read()
        elif 'password' in request.POST:
            password = request.POST['password']
            aes_key = AES_encrypt.hash_string(password)
        else:
            # Handle case where neither key file nor password was provided
            return {'error': 'Please provide a key file or a password.'}

        response = AES_encrypt.decrypt(uploaded_file, aes_key)

        return response

    return render(request, 'decrypt.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful.")
            return redirect('encrypt_file')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        new_username = request.POST.get('newUsername')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('login_page')

        # Check if the username already exists
        if User.objects.filter(username=new_username).exists():
            messages.error(request, "Username already exists.")
            return redirect('login_page')

        # Create the new user
        new_user = User(username=new_username)
        new_user.set_password(password)
        new_user.save()

        UserProfile.objects.create(user=new_user)

        messages.success(request, "Account created successfully. You can now log in.")
        return redirect('encrypt_file')

    return render(request, "login.html")

