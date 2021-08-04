import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from instagram_reviews import models as instagram_review_models
from instagram_products import models as instagram_product_models


class Command(BaseCommand):

    help = "This command creates Instagram Reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many instagram reviews do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_instagram_products = instagram_product_models.InstagramProduct.objects.all()
        all_instagram_users = instagram_product_models.InstagramUser.objects.all()
        seeder.add_entity(
            instagram_review_models.InstagramReview,
            number,
            {
                "writer": lambda x: random.choice(all_instagram_users),
                "instagram_product": lambda x: random.choice(all_instagram_products),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} instagram reviews created!"))
