from django.core.management.base import BaseCommand
from naver_products.models import AnkleHeight


class Command(BaseCommand):

    help = "This command creates ankle height"

    def handle(self, *args, **options):
        ankle_height = ["로우탑", "하이탑", "미들탑"]
        for a in ankle_height:
            AnkleHeight.objects.create(name=a)
        self.stdout.write(self.style.SUCCESS("Ankle Height created!"))
