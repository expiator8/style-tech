# Generated by Django 3.1.7 on 2021-03-15 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram_products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instagramproduct',
            options={'verbose_name_plural': 'Instagram Products'},
        ),
        migrations.AddField(
            model_name='instagramproduct',
            name='url',
            field=models.CharField(default='dd', max_length=100),
            preserve_default=False,
        ),
    ]
