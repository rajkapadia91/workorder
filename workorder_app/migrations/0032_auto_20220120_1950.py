# Generated by Django 3.1.3 on 2022-01-20 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder_app', '0031_laborrate'),
    ]

    operations = [
        migrations.CreateModel(
            name='GCInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gc_name', models.CharField(default='None', max_length=255)),
                ('gc_street_name', models.CharField(default='111 Roseland Ave', max_length=255)),
                ('gc_city_state_zipcode', models.CharField(default='Caldwell, NJ 07000', max_length=255)),
                ('gc_phone_number', models.CharField(default='123.456.789', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='jobname',
            name='gc_city_state_zip',
        ),
        migrations.RemoveField(
            model_name='jobname',
            name='gc_phone',
        ),
        migrations.RemoveField(
            model_name='jobname',
            name='gc_street',
        ),
    ]