# Generated by Django 3.2.5 on 2021-07-13 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instagram_users', '0004_auto_20210709_1247'),
        ('instagram_reviews', '0005_alter_instagramreview_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramreview',
            name='writer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instagram_reviews', to='instagram_users.instagramuser'),
        ),
    ]
