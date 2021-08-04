from django.core.management.base import BaseCommand
from naver_products.models import Feature


class Command(BaseCommand):

    help = "This command creates feature"

    def handle(self, *args, **options):
        feature = ["버클/벨티드", "키높이", "리본", "기타"]
        for f in feature:
            Feature.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS("Feature created!"))
