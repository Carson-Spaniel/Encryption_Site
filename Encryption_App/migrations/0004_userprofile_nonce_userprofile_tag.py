# Generated by Django 4.2.7 on 2024-04-24 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Encryption_App', '0003_alter_userprofile_passwordsjson'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='nonce',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='tag',
            field=models.TextField(blank=True, null=True),
        ),
    ]
