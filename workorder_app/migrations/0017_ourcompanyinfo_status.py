# Generated by Django 3.1.3 on 2021-12-28 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder_app', '0016_ourcompanyinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='ourcompanyinfo',
            name='status',
            field=models.CharField(default='Active', max_length=300),
        ),
    ]
