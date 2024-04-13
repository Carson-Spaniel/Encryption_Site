# File Encryption and Decryption Tool
This tool allows users to securely encrypt and decrypt files using AES 256 encryption. It employs SHA256 for password hashing to generate keys for the AES 256 encryption algorithm.

## Features
- Encrypt files with AES 256 encryption
- Decrypt files with the generated keys
- Password hashing using SHA256
- Drag and drop file interface for easy file selection

## Technologies Used

- **AES 256 Encryption** : The Advanced Encryption Standard (AES) with a 256-bit key size for secure file encryption.
- **SHA256 Hashing**: Secure Hash Algorithm 256 (SHA-256) for password hashing, generating keys for AES encryption.
- **HTML, CSS, JavaScript**: Frontend development for user interface and interactions.
- **Django**: Backend framework for server-side logic and file handling.

#### 1. Install the necessary dependencies.
```
pip install -r requirements.txt
```

#### 2. Run the server.
```
python manage.py runserver
```

#### 3. Access the application in your web browser at ```http://localhost:8000```

#### 4. Encryption
- Click on the "Encrypt" option in the navigation bar.
- Drag and drop the file you want to encrypt or click to upload.
- Enter a strong password for encryption (min. 8 characters, including numbers and special characters).
- Click "Encrypt" to generate the encrypted file.

#### 5. Decryption
- Click on the "Decrypt" option in the navigation bar.
- Drag and drop the encrypted file or click to upload.
- Enter the password used for encryption.
- Click "Decrypt" to retrieve the original file.

## Security Considerations
- Strong Passwords: Encourage users to use strong passwords to enhance security.
- Secure Key Generation: AES 256 keys are securely generated from SHA256-hashed passwords.
- Transport Security: Ensure the application is served over HTTPS for secure data transmission.

