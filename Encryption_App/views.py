from django.shortcuts import render
from .AES import AES_encrypt, AES_decrypt

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

        print(uploaded_file)

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
        print(response.filename)

        return response

    return render(request, 'decrypt.html')

