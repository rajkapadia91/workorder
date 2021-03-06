# Generated by Django 3.1.3 on 2020-12-12 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder_app', '0002_othermaterial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='product',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='material',
            name='quantity',
            field=models.CharField(default='0', max_length=10),
        ),
        migrations.AlterField(
            model_name='othermaterial',
            name='other_name',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='othermaterial',
            name='other_quantity',
            field=models.CharField(default='0', max_length=10),
        ),
    ]
