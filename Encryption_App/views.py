from django.shortcuts import render
from .AES import AES_encrypt, AES_decrypt

def encrypt_file(request):
    if request.method == 'POST' and request.FILES['uploaded_file']:
        uploaded_file = request.FILES['uploaded_file']

        print(uploaded_file)

        aes_key = AES_encrypt.hash_string("password")
        response = AES_encrypt.encrypt(uploaded_file, aes_key)

        return response

    return render(request, 'encrypt.html')

def decrypt_file(request):
    if request.method == 'POST' and request.FILES['uploaded_file']:
        uploaded_file = request.FILES['uploaded_file']

        print(uploaded_file)

        aes_key = AES_encrypt.hash_string("password")
        response = AES_encrypt.decrypt_file(uploaded_file, aes_key)

        return response

    return render(request, 'decrypt.html')
