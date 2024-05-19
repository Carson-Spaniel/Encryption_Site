from django.contrib.auth.models import User
from django.db import models

class WebsitePassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    website = models.TextField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)

    tag = models.TextField(blank=True, null=True)
    nonce = models.TextField(blank=True, null=True)
    ciphertext = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.website}'