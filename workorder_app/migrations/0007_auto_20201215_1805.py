# Generated by Django 3.1.3 on 2020-12-15 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workorder_app', '0006_workorder_date_work_performed'),
    ]

    operations = [
        migrations.CreateModel(
            name='LaborType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('labor_type', models.CharField(default='None', max_length=255)),
                ('labor_description', models.CharField(default='None', max_length=255)),
                ('employee_numbers', models.CharField(default='0', max_length=255)),
                ('regular_hours', models.CharField(default='0', max_length=255)),
                ('premium_hours', models.CharField(default='0', max_length=255)),
                ('double_hours', models.CharField(default='0', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='workorder',
            name='carpenterforeman',
        ),
        migrations.RemoveField(
            model_name='workorder',
            name='carpenterjourneyamn',
        ),
        migrations.RemoveField(
            model_name='workorder',
            name='laborer',
        ),
        migrations.RemoveField(
            model_name='workorder',
            name='supervisor',
        ),
        migrations.RemoveField(
            model_name='workorder',
            name='taperforeman',
        ),
        migrations.RemoveField(
            model_name='workorder',
            name='taperjourneyman',
        ),
        migrations.DeleteModel(
            name='CarpenterForeman',
        ),
        migrations.DeleteModel(
            name='CarpenterJourneyamn',
        ),
        migrations.DeleteModel(
            name='Laborer',
        ),
        migrations.DeleteModel(
            name='Supervisor',
        ),
        migrations.DeleteModel(
            name='TaperForeman',
        ),
        migrations.DeleteModel(
            name='TaperJourneyman',
        ),
        migrations.AddField(
            model_name='labortype',
            name='workorder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labortypes', to='workorder_app.workorder'),
        ),
    ]
