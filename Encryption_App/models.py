from django.contrib.auth.models import User
from django.db import models
from Crypto.PublicKey import RSA

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add fields for public key and private key
    public_key = models.TextField(blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate RSA key pair if new user and keys are not set
        if not self.pk and (not self.public_key or not self.private_key):
            pub_key, priv_key = self.generate_rsa_keypair()
            self.public_key = pub_key.decode()
            self.private_key = priv_key.decode()
        super().save(*args, **kwargs)

    def generate_rsa_keypair(self, key_size=2048):
        """
        Generates an RSA key pair for the user.

        Args:
            key_size (int): Size of the RSA key in bits (default is 2048).

        Returns:
            tuple: A tuple containing public key and private key.
        """
        key = RSA.generate(key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return public_key, private_key

    def __str__(self):
        return f'{self.user.username}'