from django.core.management.base import BaseCommand
from django_seed import Seed
from instagram_products.models import InstagramUser


class Command(BaseCommand):

    help = "This command creates Instagram Users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many instagram users do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        seeder.add_entity(
            InstagramUser,
            number,
            {
                "name": lambda x: seeder.faker.name(),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} instagram users created!"))
