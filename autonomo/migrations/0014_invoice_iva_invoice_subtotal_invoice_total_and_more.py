# Generated by Django 4.2 on 2023-05-19 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autonomo', '0013_invoice_alter_product_image_invoiceline_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='iva',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='subtotal',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='total',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='subtotal',
            field=models.FloatField(null=True),
        ),
    ]
