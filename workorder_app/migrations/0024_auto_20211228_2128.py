# Generated by Django 3.1.3 on 2021-12-28 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder_app', '0023_workorder_overhead_profit'),
    ]

    operations = [
        migrations.AddField(
            model_name='labortype',
            name='total_hours',
            field=models.CharField(default='0', max_length=255),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='overhead_profit',
            field=models.CharField(default='0', max_length=300),
        ),
    ]
