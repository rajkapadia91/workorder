# Generated by Django 3.1.3 on 2021-12-29 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorder_app', '0025_workorder_memo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workorder',
            name='invoice_date',
        ),
    ]