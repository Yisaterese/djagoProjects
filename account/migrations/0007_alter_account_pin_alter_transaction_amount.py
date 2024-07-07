# Generated by Django 5.0.6 on 2024-07-05 08:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_account_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='pin',
            field=models.CharField(default='0000', max_length=4, validators=[django.core.validators.MinLengthValidator(4), django.core.validators.MaxLengthValidator(4)]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.CharField(max_length=25),
        ),
    ]
