from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .AES import AES_encrypt
from .models import WebsitePassword, Message
from django.http import JsonResponse, HttpResponseRedirect
from Crypto.Hash import SHA256
from datetime import timedelta
from django.utils import timezone
import json
from django.utils.datastructures import MultiValueDictKeyError
import random
import string
from .generate import adjectives, nouns

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
    sha256.update(request.user.password.encode('utf-8'))
    aes_key = sha256.digest()

    time_delta = timezone.now() - timedelta(weeks=52)

    passwords = {}
    jsonPasswords = {}
    encryptedPasswords = WebsitePassword.objects.filter(user=request.user)
    for encryptedPassword in encryptedPasswords:
        if encryptedPassword.last_updated < time_delta:
            encryptedPassword.update_ready = True
            encryptedPassword.save()
        try:
            decrypted_password = AES_encrypt.decryptPassword(encryptedPassword, aes_key)
            passwords[encryptedPassword.website] = [encryptedPassword.username, decrypted_password, encryptedPassword.update_ready, encryptedPassword.last_updated]
            jsonPasswords[encryptedPassword.website] = [encryptedPassword.username, decrypted_password, 1 if encryptedPassword.update_ready else 0, encryptedPassword.last_updated.isoformat()]
        except Exception as e:
            # print(f"Failed to decrypt password for {encryptedPassword.website}: {e}")
            passwords[encryptedPassword.website] = [encryptedPassword.username, "Decryption failed", encryptedPassword.update_ready, encryptedPassword.last_updated]
            jsonPasswords[encryptedPassword.website] = [encryptedPassword.username, "Decryption failed", 1 if encryptedPassword.update_ready else 0, encryptedPassword.last_updated.isoformat()]

    sortedPasswords = dict(sorted(passwords.items()))
    sortedJsonPasswords = dict(sorted(jsonPasswords.items()))

    return render(request, "passwords.html", {'passwords':sortedPasswords, 'jsonPasswords': json.dumps(sortedJsonPasswords)})

@login_required(login_url='/login/')
def add_password_page(request):
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['uploaded_file']
            jsonPasswords = json.loads(uploaded_file.read())

            for websiteName, creds in jsonPasswords.items():
                websiteName = websiteName.replace("'","").title()
                username = creds[0]
                password = creds[1]
                update_ready = creds[2]
                last_updated = creds[3]

                sha256 = SHA256.new()
                sha256.update(request.user.password.encode('utf-8'))
                aes_key = sha256.digest()

                ciphertext, tag, nonce = AES_encrypt.encryptPassword(password, aes_key)

                sha256 = SHA256.new()
                sha256.update(websiteName.encode('utf-8'))
                hashed_website = sha256.digest()

                # Save the password
                user = request.user
                encryptedPassword, created = WebsitePassword.objects.get_or_create(user=user, hashed_website=hashed_website)
                encryptedPassword.website = websiteName
                encryptedPassword.username = username
                encryptedPassword.ciphertext = ciphertext
                encryptedPassword.tag = tag
                encryptedPassword.nonce = nonce
                encryptedPassword.last_updated = last_updated
                encryptedPassword.update_ready = update_ready
                encryptedPassword.save()

        except MultiValueDictKeyError:
            required_fields = ['websiteName', 'username', 'password', 'confirm_password']
            missing_fields = [field for field in required_fields if field not in request.POST]

            if missing_fields:
                return JsonResponse({'error': f"Missing fields: {', '.join(missing_fields)}"}, status=400)

            websiteName = request.POST['websiteName'].replace("'","").title()
            username = request.POST['username']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password != confirm_password:
                return JsonResponse({'error': 'Passwords do not match.'}, status=400)

            sha256 = SHA256.new()
            sha256.update(request.user.password.encode('utf-8'))
            aes_key = sha256.digest()

            ciphertext, tag, nonce = AES_encrypt.encryptPassword(password, aes_key)

            sha256 = SHA256.new()
            sha256.update(websiteName.encode('utf-8'))
            hashed_website = sha256.digest()

            # Save the password
            user = request.user
            encryptedPassword, created = WebsitePassword.objects.get_or_create(user=user, hashed_website=hashed_website)
            encryptedPassword.website = websiteName
            encryptedPassword.username = username
            encryptedPassword.ciphertext = ciphertext
            encryptedPassword.tag = tag
            encryptedPassword.nonce = nonce
            encryptedPassword.last_updated = timezone.now()
            encryptedPassword.update_ready = False
            encryptedPassword.save()
        except:
            return JsonResponse({'error': 'Invalid file type'}, status=400)

        return JsonResponse({'success': 'Password added.'}, status=200)
    
@login_required(login_url='/login/')
def remove_password(request):
    if request.method == 'POST':
        websiteName = request.POST['websiteName'].replace("'","").title()

        if websiteName:
            user = request.user
            sha256 = SHA256.new()
            sha256.update(websiteName.encode('utf-8'))
            hashed_website = sha256.digest()
            password = WebsitePassword.objects.filter(user=user, hashed_website=hashed_website)
            password.delete()
            return JsonResponse({'success': 'Password deleted.'}, status=200)
        else:
            return JsonResponse({'error': 'Website name not provided.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
@login_required(login_url='/login/')
def remove_all_passwords(request):
    if request.method == 'POST':
        user = request.user
        password = WebsitePassword.objects.filter(user=user)
        password.delete()
        return JsonResponse({'success': 'Passwords deleted.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
@login_required(login_url='/login/')
def messages_page(request):
    sha256 = SHA256.new()
    sha256.update(request.user.password.encode('utf-8'))
    aes_key = sha256.digest()

    messages = {}
    jsonMessages = {}
    encryptedMessages = Message.objects.filter(user=request.user)
    for encryptedMessage in encryptedMessages:
        try:
            decrypted_message = AES_encrypt.decryptPassword(encryptedMessage, aes_key)
            messages[encryptedMessage.message] = [encryptedMessage.message, decrypted_message]
            jsonMessages[encryptedMessage.message] = [encryptedMessage.message, decrypted_message]
        except Exception as e:
            # print(f"Failed to decrypt password for {encryptedPassword.website}: {e}")
            messages[encryptedMessage.message] = [encryptedMessage.message, "Decryption failed"]
            jsonMessages[encryptedMessage.message] = [encryptedMessage.message, "Decryption failed"]

    sortedMessages = dict(sorted(messages.items()))
    sortedJsonMessages = dict(sorted(jsonMessages.items()))

    return render(request, "messages.html", {'messages':sortedMessages, 'jsonMessages': json.dumps(sortedJsonMessages)})

@login_required(login_url='/login/')
def add_message_page(request):
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['uploaded_file']
            jsonMessages = json.loads(uploaded_file.read())

            for messageTitle, creds in jsonMessages.items():
                messageTitle = messageTitle.replace("'","").title()
                messageTitle = creds[0]
                message = creds[1]

                sha256 = SHA256.new()
                sha256.update(request.user.password.encode('utf-8'))
                aes_key = sha256.digest()

                ciphertext, tag, nonce = AES_encrypt.encryptPassword(message, aes_key)

                sha256 = SHA256.new()
                sha256.update(messageTitle.encode('utf-8'))
                hashed_message = sha256.digest()

                # Save the password
                user = request.user
                encryptedPassword, created = Message.objects.get_or_create(user=user, hashed_message=hashed_message)
                encryptedPassword.message = messageTitle
                encryptedPassword.ciphertext = ciphertext
                encryptedPassword.tag = tag
                encryptedPassword.nonce = nonce
                encryptedPassword.save()

        except MultiValueDictKeyError:
            required_fields = ['websiteName', 'password']
            missing_fields = [field for field in required_fields if field not in request.POST]

            if missing_fields:
                return JsonResponse({'error': f"Missing fields: {', '.join(missing_fields)}"}, status=400)

            messageTitle = request.POST['websiteName'].replace("'","").title()
            message = request.POST['password']

            sha256 = SHA256.new()
            sha256.update(request.user.password.encode('utf-8'))
            aes_key = sha256.digest()

            ciphertext, tag, nonce = AES_encrypt.encryptPassword(message, aes_key) # encrypts the message

            sha256 = SHA256.new()
            sha256.update(messageTitle.encode('utf-8'))
            hashed_message = sha256.digest()

            # Save the password
            user = request.user
            encryptedMessage, created = Message.objects.get_or_create(user=user, hashed_message=hashed_message)
            encryptedMessage.message = messageTitle
            encryptedMessage.ciphertext = ciphertext
            encryptedMessage.tag = tag
            encryptedMessage.nonce = nonce
            encryptedMessage.save()
        except:
            return JsonResponse({'error': 'Invalid file type'}, status=400)

        return JsonResponse({'success': 'Message added.'}, status=200)
    
@login_required(login_url='/login/')
def remove_message(request):
    if request.method == 'POST':
        message = request.POST['websiteName'].replace("'","").title()

        if message:
            user = request.user
            sha256 = SHA256.new()
            sha256.update(message.encode('utf-8'))
            hashed_message = sha256.digest()
            message = Message.objects.filter(user=user, hashed_message=hashed_message)
            message.delete()
            return JsonResponse({'success': 'Message deleted.'}, status=200)
        else:
            return JsonResponse({'error': 'Message title not provided.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
@login_required(login_url='/login/')
def remove_all_messages(request):
    if request.method == 'POST':
        user = request.user
        message = Message.objects.filter(user=user)
        message.delete()
        return JsonResponse({'success': 'Messages deleted.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

def generate_password(request):
    if request.method == "POST":
        password = AES_encrypt.generatePassword()
        return JsonResponse({'success': 'Password Generated', 'password': password}, status=200)
    return render(request, "generate.html")

def generate_username(request):
    if request.method == "POST":
        numbers = [''.join(random.choices(string.digits, k=2))]

        adj = random.choice(adjectives)
        noun = random.choice(nouns)
        num = random.choice(numbers)
        username = adj.title() + noun.title() + num

        return JsonResponse({'success': 'Username Generated', 'username': username}, status=200)
    return render(request, "generate.html")

def generate_pin(request):
    if request.method == "POST":
        numbers = [''.join(random.choices(string.digits, k=6))]

        return JsonResponse({'success': 'Username Generated', 'pin': numbers}, status=200)
    return render(request, "generate.html")

@login_required(login_url='/login/')
def generate_passphrase(request):
    if request.method == "POST":
        words = []
        num_words = 6
        for _ in range(num_words // 2):
            adj = random.choice(adjectives)
            noun = random.choice(nouns)
            words.append(adj)
            words.append(noun)
        passphrase = ' '.join(words)
        return JsonResponse({'success': 'Passphrase Generated', 'passphrase': passphrase}, status=200)
    return render(request, "generate.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('passwords_page')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
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
            login_url = reverse('login_page') + '?signup=1'
            return HttpResponseRedirect(login_url)

        # Create the new user
        new_user = User(username=new_username)
        new_user.set_password(password)
        new_user.save()

        auth_login(request, new_user)

        return redirect('encrypt_file')

    return render(request, "login.html")

def check_data_leak(request):
    if request.method == "POST":
        userPassword = request.POST['password']

        return AES_encrypt.check_password_leak(userPassword)