# Generated by Django 3.1.3 on 2022-05-02 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder_app', '0033_workorder_picture_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='picture_1',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
