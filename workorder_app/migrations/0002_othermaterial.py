# Generated by Django 3.1.3 on 2020-12-11 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workorder_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_name', models.CharField(max_length=255)),
                ('other_quantity', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('workorder', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='othermaterial', to='workorder_app.workorder')),
            ],
        ),
    ]
