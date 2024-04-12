from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import os
import sys
import getpass

def hash_string(input_string):
    sha256 = SHA256.new()
    sha256.update(input_string.encode('utf-8'))
    return sha256.digest()

def unpkcs_7(padded_text):
    pad_byte = padded_text[-1]
    if pad_byte < 1 or pad_byte > 16:
        raise ValueError("Invalid padding byte")

    padding = padded_text[-pad_byte:]
    if not all(padding[b] == pad_byte for b in range(len(padding))):
        raise ValueError("Invalid padding bytes")

    return padded_text[:-pad_byte]

def decrypt_file(file_path, aes_key):

    encrypted_file = file_path + "_encrypted.bin"

    with open(encrypted_file, "rb") as f:
        file_type_xor = f.read(16)
        tag = f.read(16)
        nonce = f.read(15)
        ciphertext = f.read()

    try:
        file_type_xor = unpkcs_7(file_type_xor).decode()
    except ValueError:
        return
    
    file_extension = ''.join(chr(ord(file_type_xor[i]) ^ aes_key[i % len(aes_key)]) for i in range(len(file_type_xor)))
    cipher = AES.new(aes_key, AES.MODE_OCB, nonce=nonce)

    try:
        message = cipher.decrypt_and_verify(ciphertext, tag)
        decrypted_dir = "Decrypted"
        if not os.path.exists(decrypted_dir):
            os.makedirs(decrypted_dir)
        decrypted_file_path = os.path.join(decrypted_dir, os.path.basename(file_path) + file_extension)
        with open(decrypted_file_path, "wb") as f:
            f.write(message)
        print(f"Decrypted '{file_path}_encrypted.bin'")
    except ValueError:
        print(f"\033[31mFailed to decrypt '{file_path}_encrypted.bin'\033[0m")
        
# def decrypt_folder(folder_path, aes_key):
#     for root, _, files in os.walk(folder_path):
#         for file in files:
#             if file.endswith("_encrypted.bin"):
#                 file_path = os.path.join(root, file.replace("_encrypted.bin", ""))
#                 decrypt_file(file_path, aes_key)

def main():
    if len(sys.argv) == 2:
        key_string = getpass.getpass("Enter encryption password: ")
        aes_key = hash_string(key_string)

    elif len(sys.argv) == 3:
        key_file = sys.argv[2]

        if not os.path.exists(key_file):
            print(f"Key file '{key_file}' not found.")
            sys.exit(1)

        with open(sys.argv[2], 'rb') as f:
            aes_key = f.read()
    else:
        print("Usage: \n\t\033[33mpy\033[0m AES_decrypt.py \033[34m<file_or_folder_path> <key_file>\033[0m or\n\t\033[33mpy\033[0m AES_decrypt.py \033[34m<file_or_folder_path> \033[32m(enter password)\033[0m")
        sys.exit(1)

    path = sys.argv[1]

    if os.path.isfile(path):
        # Decrypt a single file
        decrypt_file(os.path.splitext(path)[0].replace("_encrypted", ""), aes_key)
        # print(f"\n\033[32mFile '{path}' decrypted.\033[0m")
    elif os.path.isdir(path):
        # Decrypt all files in a folder
        decrypt_folder(path, aes_key)
        # print(f"\n\033[32mAll files in folder '{path}' decrypted and saved in 'Decrypted'.\033[0m")
    else:
        print(f"Error: '{path}' is not a valid file or folder.")
        sys.exit(1)

if __name__ == "__main__":
    main()
