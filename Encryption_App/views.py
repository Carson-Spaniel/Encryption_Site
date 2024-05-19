from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .AES import AES_encrypt
from .models import WebsitePassword
from django.http import JsonResponse
from Crypto.Hash import SHA256

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def passwords_page(request):
    sha256 = SHA256.new()
    sha256.update(request.user.password.split('$')[-1].encode('utf-8'))
    aes_key = sha256.digest()

    passwords = {}
    encryptedPasswords = WebsitePassword.objects.filter(user=request.user).order_by('website')
    for encryptedPassword in encryptedPasswords:
        try:
            decrypted_password = AES_encrypt.decryptPassword(encryptedPassword, aes_key)
            passwords[encryptedPassword.website] = [encryptedPassword.username, decrypted_password]
        except Exception as e:
            print(f"Failed to decrypt password for {encryptedPassword.website}: {e}")
            passwords[encryptedPassword.website] = [encryptedPassword.username, "Decryption failed"]
    print(passwords)

    return render(request, "passwords.html", {'passwords':passwords})

@login_required(login_url='/login/')
def add_password_page(request):
    if request.method == 'POST':
        required_fields = ['websiteName', 'username', 'password', 'confirm_password']
        missing_fields = [field for field in required_fields if field not in request.POST]

        if missing_fields:
            return JsonResponse({'error': f"Missing fields: {', '.join(missing_fields)}"}, status=400)

        websiteName = request.POST['websiteName'].title()
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match.'}, status=400)

        sha256 = SHA256.new()
        sha256.update(request.user.password.split('$')[-1].encode('utf-8'))
        aes_key = sha256.digest()

        ciphertext, tag, nonce = AES_encrypt.encryptPassword(password, aes_key)

        # Save the password
        user = request.user
        encryptedPassword, created = WebsitePassword.objects.get_or_create(user=user, website=websiteName)
        encryptedPassword.username = username
        encryptedPassword.ciphertext = ciphertext
        encryptedPassword.tag = tag
        encryptedPassword.nonce = nonce
        encryptedPassword.save()

        return JsonResponse({websiteName: [username, password]}, status=200)

    return render(request, "addPass.html")

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

        messages.success(request, "Account created successfully. You can now log in.")
        return redirect('encrypt_file')

    return render(request, "login.html")