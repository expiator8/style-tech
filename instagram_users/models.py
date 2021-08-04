from django.db import models
from django.urls import reverse
from core import models as core_models


# 인스타그램의 유저 모델
class InstagramUser(core_models.TimeStampedModel):

    """ Instagram User Model Definition """

    # 유저 타입(인플루언서 혹은 일반 유저)필드
    is_influencer = models.BooleanField(default=False)
    insta_id = models.CharField(max_length=30)
    followers = models.IntegerField(default=0)
    followings = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.insta_id}"

    # admin 페이지에서 보여질 모델명 수정
    class Meta:
        verbose_name = "Instagram User"
