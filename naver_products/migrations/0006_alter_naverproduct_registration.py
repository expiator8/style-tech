# Generated by Django 3.2 on 2021-05-24 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naver_products', '0005_auto_20210328_0403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='naverproduct',
            name='registration',
            field=models.DateField(blank=True, default='', null=True),
        ),
    ]
