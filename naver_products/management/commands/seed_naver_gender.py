from django.core.management.base import BaseCommand
from naver_products.models import Gender


class Command(BaseCommand):

    help = "This command creates gender"

    def handle(self, *args, **options):
        gender = ["남성용", "여성용", "남여공용"]
        for g in gender:
            Gender.objects.create(name=g)
        self.stdout.write(self.style.SUCCESS("Gender created!"))
