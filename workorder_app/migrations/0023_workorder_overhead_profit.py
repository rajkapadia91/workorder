# Generated by Django 3.1.3 on 2021-12-28 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder_app', '0022_workorder_total_invoice_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='overhead_profit',
            field=models.CharField(default='None', max_length=300),
        ),
    ]
