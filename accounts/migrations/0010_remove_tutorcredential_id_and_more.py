# Generated by Django 5.0.4 on 2024-04-25 14:19

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_tutorcredential_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorcredential',
            name='id',
        ),
        migrations.RemoveField(
            model_name='verificationstatus',
            name='id',
        ),
        migrations.AddField(
            model_name='tutorcredential',
            name='tutor_cred_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AddField(
            model_name='verificationstatus',
            name='status_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
