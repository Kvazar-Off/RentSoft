# Generated by Django 5.0.6 on 2024-05-14 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsapp', '0005_alter_employee_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='photo',
            field=models.ImageField(blank=True, default='images/photo_not_found.jpg', null=True, upload_to='userphotos/%Y-%m-%d/'),
        ),
    ]
