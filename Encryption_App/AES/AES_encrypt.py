from Crypto.Cipher import AES
from Crypto.Hash import SHA256, SHA1
import io
from django.http import FileResponse, JsonResponse
import base64
from Crypto.Random import get_random_bytes
import requests

def hash_string(input_string):
    sha256 = SHA256.new()
    sha256.update(input_string.encode('utf-8'))
    return sha256.digest()

def pkcs_7(plaintext, blocksize):
    blocks = [plaintext[i:i+blocksize] for i in range(0, len(plaintext), blocksize)]
    last_block = blocks[-1]

    if len(last_block) < blocksize:
        pad = blocksize - len(last_block)
        blocks[-1] += bytes([pad] * pad)

    return b"".join(blocks)

def unpkcs_7(padded_text):
    pad_byte = padded_text[-1]
    if pad_byte < 1 or pad_byte > 16:
        raise ValueError("Invalid padding byte")

    padding = padded_text[-pad_byte:]
    if not all(padding[b] == pad_byte for b in range(len(padding))):
        raise ValueError("Invalid padding bytes")

    return padded_text[:-pad_byte]

def encrypt(file, aes_key):
    file_info = str(file).split('.')
    file_extension = '.'+file_info[1]
    file_name = str(file).replace(file_extension, '')

    print(f'{file_name=}')
    print(f'{file_extension=}')
    
    file_extension_xor = ''.join(chr(ord(file_extension[i]) ^ aes_key[i % len(aes_key)]) for i in range(len(file_extension)))
    if not file_extension_xor:
        return

    file_ext = pkcs_7(file_extension_xor.encode(), 16)
    
    cipher = AES.new(aes_key, AES.MODE_OCB)
    ciphertext, tag = cipher.encrypt_and_digest(file.read())

    buffer = io.BytesIO()
    buffer.write(file_ext)
    buffer.write(tag)
    buffer.write(cipher.nonce)
    buffer.write(ciphertext)
    buffer.seek(0)

    response = FileResponse(buffer, as_attachment=True, filename=f"{file_name}_encrypted.bin")

    print(f'Encrypted {file}')

    return response

def decrypt(uploaded_file, aes_key):
    file_content = uploaded_file.read()
    
    file_type_xor = file_content[:16]
    tag = file_content[16:32]
    nonce = file_content[32:47]
    ciphertext = file_content[47:]

    try:
        file_type_xor = unpkcs_7(file_type_xor).decode()
    except ValueError:
        return None

    file_extension = ''.join(chr(ord(file_type_xor[i]) ^ aes_key[i % len(aes_key)]) for i in range(len(file_type_xor)))

    cipher = AES.new(aes_key, AES.MODE_OCB, nonce=nonce)

    try:
        decrypted_content = cipher.decrypt_and_verify(ciphertext, tag)

        buffer = io.BytesIO()
        buffer.write(decrypted_content)
        buffer.seek(0)

        response = FileResponse(buffer, as_attachment=True, filename=f"{str(uploaded_file).replace('_encrypted.bin', '')}{file_extension}")

        return response

    except ValueError:
        return None
    
def encryptPassword(password, aes_key):
    cipher = AES.new(aes_key, AES.MODE_OCB)
    ciphertext, tag = cipher.encrypt_and_digest(password.encode('utf-8'))
    nonce = cipher.nonce[:15]
    return base64.b64encode(ciphertext).decode('utf-8'), base64.b64encode(tag).decode('utf-8'), base64.b64encode(nonce).decode('utf-8')

def decryptPassword(encryptedPassword, aes_key):
    ciphertext = base64.b64decode(encryptedPassword.ciphertext)
    tag = base64.b64decode(encryptedPassword.tag)
    nonce = base64.b64decode(encryptedPassword.nonce)

    cipher = AES.new(aes_key, AES.MODE_OCB, nonce=nonce)
    decrypted_content = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_content.decode('utf-8')

def generatePassword():
    return base64.b64encode(get_random_bytes(32)).decode('utf-8')

def check_password_leak(password):
    hash_obj = SHA1.new()
    hash_obj.update(password.encode('utf-8'))
    full_hash = hash_obj.hexdigest()
    prefix = full_hash[:5]
    
    try: 
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    except requests.ConnectionError:
        return JsonResponse({'password_status': 2}, status=200)

    if full_hash[5:].upper() in response.text.upper():
        return JsonResponse({'password_status': 1}, status=200)
    else:
        return JsonResponse({'password_status': 0}, status=200)
