from django.core.management.base import BaseCommand
from naver_products.models import Brand


class Command(BaseCommand):

    help = "This command creates brands"

    def handle(self, *args, **options):
        brands = [
            "나이키",
            "뉴발란스",
            "컨버스",
            "아디다스",
            "디스커버리익스페디션",
            "휠라",
            "리복",
            "알렉산더맥퀸",
            "반스",
            "라코스테",
            "프로스펙스",
            "푸마",
            "스케쳐스",
            "프레드페리",
        ]
        for b in brands:
            Brand.objects.create(name=b)
        self.stdout.write(self.style.SUCCESS("Brands created!"))
