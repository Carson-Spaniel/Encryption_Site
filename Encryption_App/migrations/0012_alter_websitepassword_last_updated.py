# Generated by Django 4.2.13 on 2024-05-20 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Encryption_App', '0011_websitepassword_last_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='websitepassword',
            name='last_updated',
            field=models.DateTimeField(),
        ),
    ]
