# Generated by Django 3.2.9 on 2021-12-23 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogentry_admin_agree'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogentry',
            name='average_rate',
            field=models.IntegerField(default=False),
        ),
    ]
