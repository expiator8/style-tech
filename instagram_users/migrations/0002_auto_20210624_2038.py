# Generated by Django 3.2 on 2021-06-24 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram_users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instagramuser',
            name='follower',
        ),
        migrations.AddField(
            model_name='instagramuser',
            name='followers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='instagramuser',
            name='followings',
            field=models.IntegerField(default=0),
        ),
    ]
