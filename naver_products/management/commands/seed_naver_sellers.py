from django.core.management.base import BaseCommand
from naver_products.models import Seller


class Command(BaseCommand):

    help = "This command creates sellers"

    def handle(self, *args, **options):
        sellers = [
            "탑라인스포츠",
            "크루비",
            "11번가",
            "AK몰",
            "Gmarket",
            "롯데백화점",
            "롯데ON",
            "Cjmall",
            "슈마커공식쇼핑몰",
            "신세계몰",
        ]
        for s in sellers:
            Seller.objects.create(name=s)
        self.stdout.write(self.style.SUCCESS("Sellers created!"))
