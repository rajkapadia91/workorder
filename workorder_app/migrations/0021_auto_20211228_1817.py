# Generated by Django 3.1.3 on 2021-12-28 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder_app', '0020_auto_20211228_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='labor_cost_combined',
            field=models.CharField(default='0', max_length=255),
        ),
        migrations.AddField(
            model_name='workorder',
            name='material_cost_combined',
            field=models.CharField(default='0', max_length=255),
        ),
        migrations.AddField(
            model_name='workorder',
            name='subtotal_material_cost',
            field=models.CharField(default='0', max_length=255),
        ),
        migrations.AddField(
            model_name='workorder',
            name='subtotal_other_material_cost',
            field=models.CharField(default='0', max_length=255),
        ),
    ]