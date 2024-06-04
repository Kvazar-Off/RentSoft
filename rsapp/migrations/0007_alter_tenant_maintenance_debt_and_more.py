# Generated by Django 5.0.6 on 2024-05-26 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsapp', '0006_alter_employee_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='maintenance_debt',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Текущая задолженность по обслуживанию помещений'),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='rental_debt',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Текущая задолженность по арендным платежам'),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='total_payments',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Общая сумма выплат'),
        ),
    ]
