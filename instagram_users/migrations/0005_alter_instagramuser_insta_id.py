# Generated by Django 3.2.5 on 2021-07-13 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram_users', '0004_auto_20210709_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramuser',
            name='insta_id',
            field=models.CharField(max_length=30),
        ),
    ]
