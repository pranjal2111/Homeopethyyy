# Generated by Django 5.1.7 on 2025-03-25 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0009_medicine_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='SKU',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Unavailable', 'Unavailable')], max_length=15, null=True),
        ),
    ]
