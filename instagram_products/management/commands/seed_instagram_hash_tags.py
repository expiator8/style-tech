from django.core.management.base import BaseCommand
from django_seed import Seed
from instagram_products.models import InstagramHashTag


class Command(BaseCommand):

    help = "This command creates Instagram Hash Tags"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many instagram hash tags do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        seeder.add_entity(
            InstagramHashTag,
            number,
            {
                "name": lambda x: f"#{seeder.faker.job()}",
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} instagram hash tags created!"))
