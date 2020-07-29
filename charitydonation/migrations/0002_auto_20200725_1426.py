# Generated by Django 2.2.7 on 2020-07-25 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charitydonation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.CharField(choices=[('Fundacja', 'Fundacja'), ('Organizacja pozarządowa', 'Organizacja pozarządowa'), ('Zbiórka lokalna', 'Zbiórka lokalna')], default='Fundacja', max_length=32),
        ),
    ]
