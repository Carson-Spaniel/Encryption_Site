# Generated by Django 4.2.13 on 2024-05-20 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Encryption_App', '0012_alter_websitepassword_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='websitepassword',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
