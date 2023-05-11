# Generated by Django 4.2 on 2023-05-09 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autonomo', '0003_alter_userautonomo_birthdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nif', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('activity', models.CharField(max_length=20)),
                ('foundation_date', models.DateField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='autonomo.userautonomo')),
            ],
        ),
    ]
