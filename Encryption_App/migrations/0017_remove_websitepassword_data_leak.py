# Generated by Django 4.2.7 on 2024-06-26 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Encryption_App', '0016_websitepassword_data_leak'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='websitepassword',
            name='data_leak',
        ),
    ]