from django.db import models
from django.urls import reverse
from core import models as core_models


# 상속을 통해 여러 간단한 모델 구현을 위한 모델
class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item Model Definition """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class SearchedKeyword(AbstractItem):

    """ Instagram Hash Tag Model Definition """

    # admin 페이지에서 보여질 모델명 수정
    class Meta:
        verbose_name = "Searched Keyword"


# 인스타그램 해쉬태그 모델
class InstagramHashTag(AbstractItem):

    """ Instagram Hash Tag Model Definition """

    # admin 페이지에서 보여질 모델명 수정
    class Meta:
        verbose_name = "Instagram Hash Tag"


# 인스타그램 해쉬태그 모델
class PhotoCaption(AbstractItem):

    """ Photo Caption Model Definition """

    # admin 페이지에서 보여질 모델명 수정
    class Meta:
        verbose_name_plural = "Photo Caption"


# 인스타그램 사진 모델
class InstagramPhoto(core_models.TimeStampedModel):

    """ Instagram Photo Model Definition """

    # 사진 필드
    file = models.ImageField(upload_to="instagram_photos")
    caption = models.ManyToManyField(
        "PhotoCaption", related_name="instagram_photos", blank=True
    )
    # 사진이 등록된 InstagramProduct를 외래키로 지정.
    instagram_product = models.ForeignKey(
        "InstagramProduct", related_name="instagram_photos", on_delete=models.CASCADE
    )

    # InstagramPhoto 클래스를 호출시 반환 값을 instagram_product의 반환 값으로 설정
    def __str__(self):
        return f"{self.instagram_product}"

    # admin 페이지에서 보여질 모델명 수정
    class Meta:
        verbose_name = "Instagram Photo"


# 인스타그램 게시물 모델
class InstagramProduct(core_models.TimeStampedModel):

    """ Instagram Product Model Definition """

    # 등록일자
    date_created = models.DateField()
    # 게시물 내용
    text = models.TextField()
    # 좋아요 수
    likes = models.IntegerField(default=0)
    # 조회수
    visits = models.IntegerField(default=0)
    # 해당 게시물 url
    url = models.CharField(max_length=100)
    # 광고인지 아닌지 여부 체크
    is_ad = models.BooleanField(default=False)
    # 게시물의 모든 해시 태그
    writer = models.ForeignKey(
        "instagram_users.InstagramUser",
        related_name="instagram_products",
        on_delete=models.CASCADE,
    )
    instagram_hash_tags = models.ManyToManyField(
        "InstagramHashTag", related_name="instagram_products", blank=True
    )
    searched_keywords = models.ManyToManyField(
        "SearchedKeyword", related_name="instagram_products", blank=True
    )

    # InstagramProduct 클래스를 호출시 반환 값을 writer 반환 값으로 설정
    def __str__(self):
        return f"{self.writer}"

    # admin 페이지에서 보여질 모델명 수정
    class Meta:
        verbose_name = "Instagram Product"

    # def get_absolute_url(self):
    #     return reverse("instagram_products:detail", kwargs={"pk": self.pk})

    # 크롤링 완료 후 업데이트가 되었는지 그대로인지 체크하는 함수
    def is_newest(self):
        return self.created == self.updated

    # is_newest의 결과 표시를 true, false에서 v(체크), x 표시로 변경
    is_newest.boolean = True
