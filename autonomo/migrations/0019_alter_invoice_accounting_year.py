# Generated by Django 4.2 on 2023-05-20 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autonomo', '0018_invoice_accounting_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='accounting_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_belong_to', to='autonomo.accountingyear'),
        ),
    ]
