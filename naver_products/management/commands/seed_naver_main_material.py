from django.core.management.base import BaseCommand
from naver_products.models import MainMaterial


class Command(BaseCommand):

    help = "This command creates Main Material"

    def handle(self, *args, **options):
        main_material = [
            "가죽",
            "인조가죽(합성피혁)",
            "스웨이드",
            "폴리에스테르",
            "캔버스",
            "고무",
            "면",
            "EVA",
            "패브릭",
            "메시",
            "PVC",
            "스판덱스",
            "폴리우레탄",
            "에나멜",
            "니트",
            "기타",
        ]
        for m in main_material:
            MainMaterial.objects.create(name=m)
        self.stdout.write(self.style.SUCCESS("Main Material created!"))
