# Generated by Django 5.1.4 on 2024-12-18 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_exeatrequest_emergency_userrole_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='exeatrequest',
            name='rejection_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='exeatrequest',
            name='return_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
