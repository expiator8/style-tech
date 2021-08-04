import random
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from instagram_products import models as instagram_product_models


class Command(BaseCommand):

    help = "This command creates Instagram Product"

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
        all_instagram_users = instagram_product_models.InstagramUser.objects.all()
        seeder.add_entity(
            instagram_product_models.InstagramProduct,
            number,
            {
                "writer": lambda x: random.choice(all_instagram_users),
                "url": lambda x: seeder.faker.image_url(),
                "likes": lambda x: random.randint(0, 5000),
                "created": lambda x: make_aware(datetime.now()),
                "updated": lambda x: make_aware(
                    datetime.now() + timedelta(days=random.randint(0, 1))
                ),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        search_keywords = instagram_product_models.SearchKeyword.objects.all()
        instagram_hash_tags = instagram_product_models.InstagramHashTag.objects.all()
        for pk in created_clean:
            instagram_product = instagram_product_models.InstagramProduct.objects.get(
                pk=pk
            )
            instagram_product_models.InstagramPhoto.objects.create(
                file=f"instagram_photos/{random.randint(1,20)}.jpg",
                instagram_product=instagram_product,
            )
            for s in search_keywords:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    instagram_product.search_keyword.add(s)
            for i in instagram_hash_tags:
                random_number = random.randint(0, 15)
                if random_number % 2 == 0:
                    instagram_product.instagram_hash_tag.add(i)
        self.stdout.write(self.style.SUCCESS(f"{number} instagram products created!"))
