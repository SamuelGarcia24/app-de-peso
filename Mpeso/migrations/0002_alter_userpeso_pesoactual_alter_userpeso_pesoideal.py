# Generated by Django 5.0.1 on 2024-01-29 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mpeso', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpeso',
            name='pesoActual',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='userpeso',
            name='pesoIdeal',
            field=models.IntegerField(),
        ),
    ]
