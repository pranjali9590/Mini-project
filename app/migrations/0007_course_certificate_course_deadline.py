# Generated by Django 4.2.7 on 2024-01-11 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_language_course_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='Certificate',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='Deadline',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
