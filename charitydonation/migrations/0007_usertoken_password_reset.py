# Generated by Django 2.2.13 on 2020-08-11 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charitydonation', '0006_usertoken_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertoken',
            name='password_reset',
            field=models.BooleanField(default=False),
        ),
    ]
