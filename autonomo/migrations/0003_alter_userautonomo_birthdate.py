# Generated by Django 4.2 on 2023-05-07 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autonomo', '0002_userautonomo_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userautonomo',
            name='birthdate',
            field=models.CharField(max_length=20),
        ),
    ]
