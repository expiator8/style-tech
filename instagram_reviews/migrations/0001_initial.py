# Generated by Django 3.1.7 on 2021-03-15 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('instagram_products', '0003_auto_20210316_0037'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('writer', models.CharField(max_length=30)),
                ('instagram_review', models.TextField()),
                ('date_created', models.DateField()),
                ('instagram_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instagram_reviews', to='instagram_products.instagramproduct')),
            ],
            options={
                'verbose_name_plural': 'Instagram Reviews',
            },
        ),
    ]
