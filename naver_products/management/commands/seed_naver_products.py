import random
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from naver_products import models as naver_product_models


class Command(BaseCommand):

    help = "This command creates Naver Product"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many naver products do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        all_manufacturers = naver_product_models.Manufacturer.objects.all()
        all_brands = naver_product_models.Brand.objects.all()
        seeder.add_entity(
            naver_product_models.NaverProduct,
            number,
            {
                "name": lambda x: seeder.faker.license_plate(),
                "url": lambda x: seeder.faker.image_url(),
                "manufacturer": lambda x: random.choice(all_manufacturers),
                "brand": lambda x: random.choice(all_brands),
                "price": lambda x: random.randint(10000, 100000),
                "dibs": lambda x: random.randint(0, 5000),
                "created": lambda x: make_aware(datetime.now()),
                "updated": lambda x: make_aware(
                    datetime.now() + timedelta(days=random.randint(0, 1))
                ),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        search_keywords = naver_product_models.SearchKeyword.objects.all()
        categories = naver_product_models.Category.objects.all()
        sellers = naver_product_models.Seller.objects.all()
        heel_height = naver_product_models.HeelHeight.objects.all()
        ankle_height = naver_product_models.AnkleHeight.objects.all()
        gender = naver_product_models.Gender.objects.all()
        main_material = naver_product_models.MainMaterial.objects.all()
        sole_material = naver_product_models.SoleMaterial.objects.all()
        add_ons = naver_product_models.AddOns.objects.all()
        feature = naver_product_models.Feature.objects.all()
        for pk in created_clean:
            naver_product = naver_product_models.NaverProduct.objects.get(pk=pk)
            naver_product_models.NaverPhoto.objects.create(
                file=f"naver_photos/{random.randint(1,20)}.jpg",
                naver_product=naver_product,
            )
            for s in search_keywords:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    naver_product.search_keywords.add(s)
            for c in categories:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    naver_product.category.add(c)
            for s in sellers:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    naver_product.seller.add(s)
            for h in heel_height:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    naver_product.heel_height.add(h)
            for m in main_material:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    naver_product.main_material.add(m)
            for a in add_ons:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    naver_product.add_ons.add(a)
            for f in feature:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    naver_product.feature.add(f)
            naver_product.ankle_height.add(random.choice(ankle_height))
            naver_product.sole_material.add(random.choice(sole_material))
            naver_product.gender.add(random.choice(gender))
        self.stdout.write(self.style.SUCCESS(f"{number} naver products created!"))
