# Generated by Django 3.1.7 on 2021-03-27 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('naver_products', '0004_auto_20210320_0036'),
        ('naver_reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='naverreview',
            name='buy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='naver_reviews', to='naver_products.seller'),
        ),
    ]
