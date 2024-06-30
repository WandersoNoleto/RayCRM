# Generated by Django 5.0.4 on 2024-06-30 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0004_consultationdaysummary'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='type',
            field=models.CharField(choices=[('Consulta', 'Consulta'), ('Retorno', 'Retorno')], default='Consulta', max_length=10),
        ),
    ]
