# Generated by Django 3.2 on 2021-06-24 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram_products', '0006_auto_20210321_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instagramproduct',
            name='search_keywords',
        ),
    ]