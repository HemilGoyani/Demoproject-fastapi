# Generated by Django 3.2.10 on 2022-03-29 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_seller', '0004_alter_carseller_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carseller',
            name='picture',
            field=models.ImageField(upload_to='media/'),
        ),
    ]
