# Generated by Django 5.0.4 on 2024-04-22 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0003_sessionbook_duration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sessionbook',
            options={'verbose_name_plural': 'Booked Sessions'},
        ),
        migrations.AlterField(
            model_name='sessionbook',
            name='duration',
            field=models.CharField(blank=True, help_text='10days', max_length=20, null=True),
        ),
    ]