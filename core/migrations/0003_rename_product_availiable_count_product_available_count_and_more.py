# Generated by Django 5.1.3 on 2024-11-23 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_category_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_availiable_count',
            new_name='available_count',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='desc',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='img',
            new_name='image',
        ),
    ]
