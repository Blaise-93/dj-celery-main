# Generated by Django 4.2 on 2024-08-03 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('STUDENT', 'Student'), ('Teacher', 'Teacher')], default='Blaise', max_length=50),
            preserve_default=False,
        ),
    ]
