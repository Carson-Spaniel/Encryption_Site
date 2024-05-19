from django.contrib.auth.models import User
from django.db import models
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add fields for public key and private key
    public_key = models.TextField(blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)
    tag = models.TextField(blank=True, null=True)
    nonce = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        sha256 = SHA256.new()
        sha256.update(self.user.password.split('$')[-1][0:32].encode('utf-8'))
        aes_key = sha256.digest()
        cipher = AES.new(aes_key, AES.MODE_OCB)
        
        passwordsCiphertext, tag = cipher.encrypt_and_digest(self.passwordsJson.encode('utf-8'))

        self.passwordsJson = tag + passwordsCiphertext
        self.nonce = cipher.nonce

        # Generate RSA key pair if new user and keys are not set
        if not self.pk and (not self.public_key or not self.private_key):
            pub_key, priv_key = self.generate_rsa_keypair()

            '''
                1. Get password of user
                2. Hash the password using SHA 256
                3. Encrypt the data using AES with the hashed password as the key
                4. Save encrypted data to designated areas                
            '''

            publicCiphertext, tag = cipher.encrypt_and_digest(pub_key.decode())
            self.public_key = tag + publicCiphertext

            privateCiphertext, tag = cipher.encrypt_and_digest(priv_key.decode())
            self.private_key = tag + privateCiphertext
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}'