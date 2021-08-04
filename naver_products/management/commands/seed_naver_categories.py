from django.core.management.base import BaseCommand
from naver_products.models import Category


class Command(BaseCommand):

    help = "This command creates categories"

    def handle(self, *args, **options):
        categories = [
            "남성러닝화",
            "남성스니커즈",
            "남성워킹화",
            "남성슬립온",
            "남성워커",
            "남성정장구두",
            "남성작업화",
            "남성부츠",
            "남성웰트화",
            "남성아쿠아슈즈",
            "남성컴포트화",
            "남성슬리퍼",
            "여자겨울스니커즈",
            "러닝화",
            "여성드라이빙슈즈",
            "여성러닝화",
            "여성운동화",
            "여성신발",
            "여성앵클/숏부츠",
            "여성컴포트화",
            "여성플랫",
            "여성슬립온",
            "여성로퍼",
            "여성슬리퍼",
            "여성옥스퍼드화",
        ]
        for c in categories:
            Category.objects.create(name=c)
        self.stdout.write(self.style.SUCCESS("Categories created!"))
