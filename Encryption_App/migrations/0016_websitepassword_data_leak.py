# Generated by Django 4.2.13 on 2024-06-26 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Encryption_App', '0015_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='websitepassword',
            name='data_leak',
            field=models.IntegerField(default=0),
        ),
    ]
