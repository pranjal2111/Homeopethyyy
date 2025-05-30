# Generated by Django 5.1.6 on 2025-03-31 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0037_alter_department_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='city',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='landmark',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='number',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='phone',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='pincode',
            field=models.IntegerField(max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='societyname',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='street',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='quantity',
            field=models.IntegerField(max_length=4, null=True),
        ),
    ]
