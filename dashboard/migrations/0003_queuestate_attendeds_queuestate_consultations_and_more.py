# Generated by Django 5.0.4 on 2024-07-01 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_queuestate'),
    ]

    operations = [
        migrations.AddField(
            model_name='queuestate',
            name='attendeds',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='queuestate',
            name='consultations',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='queuestate',
            name='follow_ups',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='queuestate',
            name='total',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='queuestate',
            name='waiting',
            field=models.IntegerField(default=0),
        ),
    ]