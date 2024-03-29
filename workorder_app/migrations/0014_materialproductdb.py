# Generated by Django 3.1.3 on 2021-12-27 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder_app', '0013_auto_20210813_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialProductDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=300)),
                ('unit_of_measurement', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
