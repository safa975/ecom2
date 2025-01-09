# Generated by Django 5.1.3 on 2025-01-04 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_customer_user_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default='COD', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('C', 'Completed'), ('F', 'Failed'), ('D', 'Delivered')], default='COMPLETED', max_length=1),
        ),
    ]
