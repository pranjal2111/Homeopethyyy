# Generated by Django 5.1.7 on 2025-03-24 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_rename_full_name_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
