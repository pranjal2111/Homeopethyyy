# Generated by Django 5.1.7 on 2025-03-30 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0035_alter_doctor_department_alter_doctor_specialist'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='img',
            field=models.ImageField(null=True, upload_to='doctors'),
        ),
    ]
