from django.core.management.base import BaseCommand
from naver_products.models import SoleMaterial


class Command(BaseCommand):

    help = "This command creates sole material"

    def handle(self, *args, **options):
        sole_material = ["고무", "파일론", "EVA", "TPU", "기타"]
        for s in sole_material:
            SoleMaterial.objects.create(name=s)
        self.stdout.write(self.style.SUCCESS("Sole Material created!"))
