# Generated by Django 4.1.5 on 2023-02-14 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_subscribed',
            field=models.BooleanField(default=False),
        ),
    ]