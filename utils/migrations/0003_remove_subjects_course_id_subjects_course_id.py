# Generated by Django 4.0.1 on 2022-01-23 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_subjects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjects',
            name='course_ID',
        ),
        migrations.AddField(
            model_name='subjects',
            name='course_ID',
            field=models.ManyToManyField(to='utils.Course'),
        ),
    ]
