# Generated by Django 3.1.1 on 2021-06-07 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.TextField(blank=True, null=True),
        ),
    ]
