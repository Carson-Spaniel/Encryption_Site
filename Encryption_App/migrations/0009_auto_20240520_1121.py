# Generated by Django 3.2.25 on 2024-05-20 16:21

from django.db import migrations
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Encryption_App', '0008_alter_websitepassword_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='websitepassword',
            name='ciphertext',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='websitepassword',
            name='nonce',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='websitepassword',
            name='tag',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='websitepassword',
            name='username',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='websitepassword',
            name='website',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True, null=True),
        ),
    ]
