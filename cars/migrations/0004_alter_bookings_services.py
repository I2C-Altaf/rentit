# Generated by Django 4.1.5 on 2023-02-21 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_alter_bookings_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='services',
            field=models.ManyToManyField(blank=True, null=True, to='cars.services'),
        ),
    ]
