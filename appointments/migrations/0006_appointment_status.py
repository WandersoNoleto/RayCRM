# Generated by Django 5.0.4 on 2024-07-01 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0005_appointment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('attended', 'Attended'), ('waiting', 'Waiting'), ('missed', 'Missed')], default='waiting', max_length=20),
        ),
    ]
