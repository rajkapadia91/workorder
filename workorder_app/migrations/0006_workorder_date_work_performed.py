# Generated by Django 3.1.3 on 2020-12-14 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder_app', '0005_auto_20201214_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='date_work_performed',
            field=models.CharField(default='None', max_length=255),
        ),
    ]
