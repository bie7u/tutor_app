# Generated by Django 3.2.9 on 2021-12-23 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_blogentry_average_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogentry',
            name='average_rate',
            field=models.CharField(blank=True, default=False, max_length=200000000000000000),
        ),
    ]
