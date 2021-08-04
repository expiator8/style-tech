from django.core.management.base import BaseCommand
from naver_products.models import HeelHeight


class Command(BaseCommand):

    help = "This command creates Heel Height"

    def handle(self, *args, **options):
        heel_height = [
            "1cm이하",
            "1cm대",
            "2cm대",
            "3cm대",
            "4cm대",
            "5cm대",
            "6cm대",
            "7cm대",
            "8cm대",
            "9cm대",
            "10cm이상",
        ]
        for h in heel_height:
            HeelHeight.objects.create(name=h)
        self.stdout.write(self.style.SUCCESS("Heel Height created!"))
