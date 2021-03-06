# Generated by Django 3.1.7 on 2021-03-17 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('naver_products', '0002_auto_20210317_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='naverproduct',
            name='add_ons',
            field=models.ManyToManyField(blank=True, related_name='naver_products', to='naver_products.AddOns'),
        ),
        migrations.AlterField(
            model_name='naverproduct',
            name='ankle_height',
            field=models.ManyToManyField(blank=True, related_name='naver_products', to='naver_products.AnkleHeight'),
        ),
        migrations.AlterField(
            model_name='naverproduct',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='naver_products', to='naver_products.brand'),
        ),
        migrations.AlterField(
            model_name='naverproduct',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='naver_products', to='naver_products.Category'),
        ),
        migrations.AlterField(
            model_name='naverproduct',
            name='feature',
            field=models.ManyToManyField(blank=True, related_name='naver_products', to='naver_products.Feature'),
        ),
        migrations.AlterField(
            model_name='naverproduct',
            name='gender',
            field=models.ManyToManyField(blank=True, related_name='naver_products', to='naver_products.Gender'),
        ),
        migrations.AlterField(
            model_name='naverproduct',
            name='heel_height',
            field=models.ManyToManyField(blank=True, related_name='naver_products', to='naver_products.HeelHeight'),
        ),
        migrations.AlterField(
            model_name='naverproduct',
            name='main_material',
            field=models.ManyToManyField(blank=True, related_name='naver_products', to='naver_products.MainMaterial'),
        ),
        migrations.AlterField(
            model_name='naverproduct',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='naver_products', to='naver_products.manufacturer'),
        ),
        migrations.AlterField(
            model_name='naverproduct',
            name='seller',
            field=models.ManyToManyField(blank=True, related_name='naver_products', to='naver_products.Seller'),
        ),
        migrations.AlterField(
            model_name='naverproduct',
            name='sole_material',
            field=models.ManyToManyField(blank=True, related_name='naver_products', to='naver_products.SoleMaterial'),
        ),
    ]
