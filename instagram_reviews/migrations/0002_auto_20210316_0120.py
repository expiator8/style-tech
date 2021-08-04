# Generated by Django 3.1.7 on 2021-03-15 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instagram_products', '0004_auto_20210316_0120'),
        ('instagram_reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramreview',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instagram_reviews', to='instagram_products.instagramuser'),
        ),
    ]