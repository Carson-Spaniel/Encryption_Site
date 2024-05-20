# Generated by Django 4.2.13 on 2024-05-20 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Encryption_App', '0010_websitepassword_hashed_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='websitepassword',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='websitepassword',
            name='update_ready',
            field=models.BooleanField(default=False),
        ),
    ]
