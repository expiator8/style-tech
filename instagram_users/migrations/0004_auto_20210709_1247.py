# Generated by Django 3.2 on 2021-07-09 03:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram_users', '0003_auto_20210709_1115'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instagramuser',
            options={'verbose_name': 'Instagram User'},
        ),
        migrations.RenameField(
            model_name='instagramuser',
            old_name='influencer',
            new_name='is_influencer',
        ),
    ]
