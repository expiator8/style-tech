# Generated by Django 3.1.7 on 2021-03-21 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram_products', '0005_auto_20210317_2324'),
    ]

    operations = [
        migrations.RenameField(
            model_name='instagramproduct',
            old_name='instagram_hash_tag',
            new_name='instagram_hash_tags',
        ),
        migrations.RenameField(
            model_name='instagramproduct',
            old_name='search_keyword',
            new_name='search_keywords',
        ),
    ]