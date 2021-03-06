# Generated by Django 3.1.1 on 2021-06-04 19:32

import django.contrib.postgres.search
from django.db import migrations, models
from django.contrib.postgres.operations import TrigramExtension # Manually added for Search function.


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        TrigramExtension(), #Manually added for search function.
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.AutoField(primary_key=True, serialize=False)),
                ('pub_date', models.DateTimeField()),
                ('article_title', models.TextField(blank=True, null=True)),
                ('article_abstract', models.TextField(blank=True, null=True)),
                ('author_list', models.TextField(blank=True, null=True)),
                ('keyword_list', models.TextField(blank=True, null=True)),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
            ],
        ),
    ]
