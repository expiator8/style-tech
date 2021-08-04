import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from naver_reviews import models as naver_review_models
from naver_products import models as naver_product_models


class Command(BaseCommand):

    help = "This command creates Naver Reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many naver reviews do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_naver_products = naver_product_models.NaverProduct.objects.all()
        seeder.add_entity(
            naver_review_models.NaverReview,
            number,
            {
                "rating": lambda x: random.randint(1, 5),
                "naver_product": lambda x: random.choice(all_naver_products),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} naver reviews created!"))
