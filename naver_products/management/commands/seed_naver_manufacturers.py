from django.core.management.base import BaseCommand
from naver_products.models import Manufacturer


class Command(BaseCommand):

    help = "This command creates manufacturers"

    def handle(self, *args, **options):
        manufacturers = [
            "나이키",
            "뉴발란스",
            "컨버스",
            "F&F",
            "스케쳐스",
            "반스",
            "골든구스",
            "코오롱인더스트리",
            "구찌",
        ]
        for m in manufacturers:
            Manufacturer.objects.create(name=m)
        self.stdout.write(self.style.SUCCESS("Manufacturers created!"))
