# Generated by Django 3.1.3 on 2020-12-14 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder_app', '0003_auto_20201212_0219'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='measurement',
            field=models.CharField(default='None', max_length=20),
        ),
        migrations.AddField(
            model_name='material',
            name='measurement_amount',
            field=models.CharField(default='None', max_length=20),
        ),
    ]
