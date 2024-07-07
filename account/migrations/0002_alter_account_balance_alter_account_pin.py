# Generated by Django 5.0.6 on 2024-06-26 12:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='account',
            name='pin',
            field=models.CharField(max_length=4, validators=[django.core.validators.MinLengthValidator(4), django.core.validators.MaxLengthValidator(4)]),
        ),
    ]
