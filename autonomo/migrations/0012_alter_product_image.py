# Generated by Django 4.2 on 2023-05-15 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autonomo', '0011_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]