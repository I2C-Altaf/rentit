# Generated by Django 4.1.5 on 2023-02-15 04:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_contact_contacted_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator]),
        ),
    ]
