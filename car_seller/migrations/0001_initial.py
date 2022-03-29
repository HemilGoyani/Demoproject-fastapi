# Generated by Django 3.2.10 on 2022-03-28 10:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarSeller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_name', models.CharField(max_length=20)),
                ('seller_mobile', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(10)])),
                ('make', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('year', models.IntegerField(default=0)),
                ('Condition', models.CharField(choices=[('P', 'poor'), ('F', 'fair'), ('G', 'good'), ('E', 'excellent')], max_length=10)),
                ('asking_pricce', models.FloatField(max_length=7)),
            ],
        ),
    ]