# Generated by Django 3.2.9 on 2021-11-21 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reg_log', '0002_auto_20211118_2008'),
        ('tutoring_ads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='data',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='reg_log.client'),
        ),
    ]
