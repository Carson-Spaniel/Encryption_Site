from django.contrib.auth.models import User
from django.db import models
from encrypted_model_fields.fields import EncryptedTextField

class WebsitePassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hashed_website = models.TextField(blank=True, null=True)
    website = EncryptedTextField(blank=True, null=True)
    username = EncryptedTextField(blank=True, null=True)

    tag = EncryptedTextField(blank=True, null=True)
    nonce = EncryptedTextField(blank=True, null=True)
    ciphertext = EncryptedTextField(blank=True, null=True)

    last_updated = models.DateTimeField(null=True)
    update_ready = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.website}'