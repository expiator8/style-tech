from django.core.management.base import BaseCommand
from naver_products.models import AddOns


class Command(BaseCommand):

    help = "This command creates add-ons"

    def handle(self, *args, **options):
        add_ons = ["통풍", "키높이", "충격흡수", "경량", "스카치", "에어", "해당없음"]
        for a in add_ons:
            AddOns.objects.create(name=a)
        self.stdout.write(self.style.SUCCESS("Add-Ons created!"))
